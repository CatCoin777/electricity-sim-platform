# routers/evaluation.py

from fastapi import APIRouter, HTTPException, Depends, Query
from fastapi.security import OAuth2PasswordBearer
from schemas.evaluation import (
    EvaluationCriteria, StudentScore, ClassEvaluation, 
    ExperimentReport
)
from services.evaluation.score_calculator import (
    calculate_student_score, calculate_class_rankings,
    generate_score_distribution, calculate_class_average
)
from mock_data.file_storage import get_scenario, get_bids, save_evaluation_criteria, get_evaluation_criteria
from mock_data.mock_users import mock_users
from security import decode_access_token
from typing import List, Dict
import json
from datetime import datetime

router = APIRouter(prefix="/api/evaluation", tags=["Evaluation"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


@router.post("/criteria")
async def set_evaluation_criteria(
    criteria: EvaluationCriteria,
    token: str = Depends(oauth2_scheme)
):
    """设置评估标准（教师专用）"""
    payload = decode_access_token(token)
    if not payload or payload.get("role") != "teacher":
        raise HTTPException(status_code=403, detail="只有教师可以设置评估标准")
    
    save_evaluation_criteria(criteria.scenario_id, criteria.dict())
    return {"message": "评估标准设置成功"}


@router.get("/criteria/{scenario_id}")
async def get_evaluation_criteria(scenario_id: str):
    """获取评估标准"""
    criteria = get_evaluation_criteria(scenario_id)
    if not criteria:
        raise HTTPException(status_code=404, detail="未找到评估标准")
    return criteria


@router.post("/calculate/{scenario_id}")
async def calculate_class_scores(
    scenario_id: str,
    mechanism_type: str = Query("uniform_price"),
    token: str = Depends(oauth2_scheme)
):
    """计算班级成绩（教师专用）"""
    payload = decode_access_token(token)
    if not payload or payload.get("role") != "teacher":
        raise HTTPException(status_code=403, detail="只有教师可以计算成绩")
    
    # 获取场景信息
    scenario = get_scenario(scenario_id)
    if not scenario:
        raise HTTPException(status_code=404, detail="场景不存在")
    
    # 获取所有竞价
    bid_data = get_bids(scenario_id)
    if not bid_data:
        raise HTTPException(status_code=404, detail="未找到竞价数据")
    
    # 获取评估标准
    criteria_data = get_evaluation_criteria(scenario_id)
    if not criteria_data:
        # 使用默认评估标准
        criteria = EvaluationCriteria(
            scenario_id=scenario_id,
            mechanism_type=mechanism_type
        )
    else:
        criteria = EvaluationCriteria(**criteria_data)
    
    # 计算市场出清结果
    from routers.simulation import get_result
    try:
        result = get_result(scenario_id, mechanism_type)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"市场出清计算失败: {str(e)}")
    
    # 计算每个学生的成绩
    student_scores = []
    for student_id, bid in bid_data.items():
        if student_id in scenario["participants"]:
            score = calculate_student_score(
                student_id=student_id,
                scenario_id=scenario_id,
                mechanism_type=mechanism_type,
                submitted_bid=bid,
                actual_result=result,
                criteria=criteria
            )
            student_scores.append(score)
    
    # 计算排名
    rankings = calculate_class_rankings(student_scores)
    for score in student_scores:
        score.rank = rankings.get(score.student_id, 0)
    
    # 计算班级统计
    class_average = calculate_class_average(student_scores)
    score_distribution = generate_score_distribution(student_scores)
    
    # 保存评估结果
    evaluation_result = ClassEvaluation(
        class_id=f"class_{scenario_id}",
        scenario_id=scenario_id,
        mechanism_type=mechanism_type,
        evaluation_criteria=criteria,
        student_scores=student_scores,
        class_average=class_average,
        class_rankings=rankings
    )
    
    # 保存到文件
    save_evaluation_result(scenario_id, mechanism_type, evaluation_result.dict())
    
    return {
        "message": "成绩计算完成",
        "class_average": class_average,
        "total_students": len(student_scores),
        "score_distribution": score_distribution,
        "rankings": rankings
    }


@router.get("/scores/{scenario_id}")
async def get_student_scores(
    scenario_id: str,
    mechanism_type: str = Query("uniform_price"),
    token: str = Depends(oauth2_scheme)
):
    """获取学生成绩"""
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="无效令牌")
    
    # 获取评估结果
    evaluation_result = get_evaluation_result(scenario_id, mechanism_type)
    if not evaluation_result:
        raise HTTPException(status_code=404, detail="未找到评估结果")
    
    # 如果是学生，只返回自己的成绩
    if payload.get("role") == "student":
        student_id = payload.get("sub")
        student_score = next(
            (score for score in evaluation_result["student_scores"] 
             if score["student_id"] == student_id), 
            None
        )
        if not student_score:
            raise HTTPException(status_code=404, detail="未找到您的成绩")
        return student_score
    
    # 如果是教师，返回所有成绩
    return evaluation_result


@router.get("/report/{scenario_id}")
async def generate_experiment_report(
    scenario_id: str,
    mechanism_type: str = Query("uniform_price"),
    token: str = Depends(oauth2_scheme)
):
    """生成实验报告（教师专用）"""
    payload = decode_access_token(token)
    if not payload or payload.get("role") != "teacher":
        raise HTTPException(status_code=403, detail="只有教师可以生成报告")
    
    # 获取评估结果
    evaluation_result = get_evaluation_result(scenario_id, mechanism_type)
    if not evaluation_result:
        raise HTTPException(status_code=404, detail="未找到评估结果")
    
    # 获取场景信息
    scenario = get_scenario(scenario_id)
    if not scenario:
        raise HTTPException(status_code=404, detail="场景不存在")
    
    # 获取竞价数据
    bid_data = get_bids(scenario_id)
    
    # 计算统计数据
    total_participants = len(scenario["participants"])
    submitted_count = len(bid_data)
    submission_rate = round(submitted_count / total_participants * 100, 2)
    
    # 获取前几名学生
    sorted_scores = sorted(
        evaluation_result["student_scores"], 
        key=lambda x: x["total_score"], 
        reverse=True
    )
    top_performers = [score["student_id"] for score in sorted_scores[:3]]
    
    # 生成分析总结
    analysis_summary = generate_analysis_summary(
        evaluation_result, scenario, bid_data
    )
    
    report = ExperimentReport(
        scenario_id=scenario_id,
        mechanism_type=mechanism_type,
        total_participants=total_participants,
        submitted_count=submitted_count,
        submission_rate=submission_rate,
        average_score=evaluation_result["class_average"],
        score_distribution=evaluation_result.get("score_distribution", {}),
        top_performers=top_performers,
        analysis_summary=analysis_summary
    )
    
    return report


@router.get("/export/{scenario_id}")
async def export_grades(
    scenario_id: str,
    mechanism_type: str = Query("uniform_price"),
    format: str = Query("json"),
    token: str = Depends(oauth2_scheme)
):
    """导出成绩（教师专用）"""
    payload = decode_access_token(token)
    if not payload or payload.get("role") != "teacher":
        raise HTTPException(status_code=403, detail="只有教师可以导出成绩")
    
    # 获取评估结果
    evaluation_result = get_evaluation_result(scenario_id, mechanism_type)
    if not evaluation_result:
        raise HTTPException(status_code=404, detail="未找到评估结果")
    
    if format.lower() == "csv":
        # 生成CSV格式
        csv_content = generate_csv_export(evaluation_result)
        return {
            "format": "csv",
            "content": csv_content,
            "filename": f"grades_{scenario_id}_{mechanism_type}.csv"
        }
    else:
        # 返回JSON格式
        return {
            "format": "json",
            "data": evaluation_result,
            "filename": f"grades_{scenario_id}_{mechanism_type}.json"
        }


# 辅助函数
def save_evaluation_result(scenario_id: str, mechanism_type: str, result: Dict):
    """保存评估结果到文件"""
    filename = f"mock_data/evaluation_{scenario_id}_{mechanism_type}.json"
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2, default=str)


def get_evaluation_result(scenario_id: str, mechanism_type: str) -> Dict:
    """从文件获取评估结果"""
    filename = f"mock_data/evaluation_{scenario_id}_{mechanism_type}.json"
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return None


def generate_analysis_summary(evaluation_result: Dict, scenario: Dict, bid_data: Dict) -> str:
    """生成分析总结"""
    scores = evaluation_result["student_scores"]
    avg_score = evaluation_result["class_average"]
    
    # 分析成绩分布
    excellent_count = len([s for s in scores if s["total_score"] >= 90])
    good_count = len([s for s in scores if 80 <= s["total_score"] < 90])
    pass_count = len([s for s in scores if s["total_score"] >= 60])
    
    summary = f"""
    实验场景 {scenario['scenario_id']} 分析报告：
    
    总体表现：
    - 班级平均分：{avg_score:.2f}
    - 优秀学生（90分以上）：{excellent_count}人
    - 良好学生（80-89分）：{good_count}人
    - 及格率：{pass_count}/{len(scores)} ({pass_count/len(scores)*100:.1f}%)
    
    市场机制：{evaluation_result['mechanism_type']}
    需求量：{scenario['demand']} MW
    参与人数：{len(scenario['participants'])}人
    提交率：{len(bid_data)}/{len(scenario['participants'])} ({len(bid_data)/len(scenario['participants'])*100:.1f}%)
    """
    
    return summary.strip()


def generate_csv_export(evaluation_result: Dict) -> str:
    """生成CSV格式的导出数据"""
    csv_lines = ["学生ID,场景ID,机制类型,价格得分,利润得分,总分,排名"]
    
    for score in evaluation_result["student_scores"]:
        csv_lines.append(
            f"{score['student_id']},{score['scenario_id']},{score['mechanism_type']},"
            f"{score['price_score']:.2f},{score['profit_score']:.2f},"
            f"{score['total_score']:.2f},{score['rank']}"
        )
    
    return "\n".join(csv_lines) 