# routers/classes.py

from fastapi import APIRouter, HTTPException, Depends, Body
from fastapi.security import OAuth2PasswordBearer
from schemas.classes import (
    ClassInfo, ClassMember, ExperimentAssignment, StudentProgress
)
from mock_data.mock_users import mock_users
from security import decode_access_token
from typing import List, Dict
import json
from datetime import datetime, timedelta
import uuid

router = APIRouter(prefix="/classes", tags=["Classes"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


@router.post("/create")
async def create_class(
    class_name: str = Body(...),
    description: str = Body(None),
    token: str = Depends(oauth2_scheme)
):
    """创建班级（教师专用）"""
    payload = decode_access_token(token)
    if not payload or payload.get("role") != "teacher":
        raise HTTPException(status_code=403, detail="只有教师可以创建班级")
    
    teacher_id = payload.get("sub")
    class_id = f"class_{uuid.uuid4().hex[:8]}"
    
    class_info = ClassInfo(
        class_id=class_id,
        class_name=class_name,
        teacher_id=teacher_id,
        students=[],
        created_at=datetime.now(),
        description=description
    )
    
    # 保存班级信息
    save_class_info(class_info.dict())
    
    return {
        "message": "班级创建成功",
        "class_id": class_id,
        "class_info": class_info.dict()
    }


@router.get("/my-classes")
async def get_my_classes(token: str = Depends(oauth2_scheme)):
    """获取我的班级"""
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="无效令牌")
    
    user_id = payload.get("sub")
    user_role = payload.get("role")
    
    all_classes = load_all_classes()
    my_classes = []
    
    if user_role == "teacher":
        # 教师：获取自己创建的班级
        my_classes = [cls for cls in all_classes if cls["teacher_id"] == user_id]
    else:
        # 学生：获取自己所在的班级
        my_classes = [cls for cls in all_classes if user_id in cls["students"]]
    
    return my_classes


@router.post("/{class_id}/add-students")
async def add_students_to_class(
    class_id: str,
    student_ids: List[str] = Body(...),
    token: str = Depends(oauth2_scheme)
):
    """添加学生到班级（教师专用）"""
    payload = decode_access_token(token)
    if not payload or payload.get("role") != "teacher":
        raise HTTPException(status_code=403, detail="只有教师可以添加学生")
    
    # 获取班级信息
    class_info = get_class_info(class_id)
    if not class_info:
        raise HTTPException(status_code=404, detail="班级不存在")
    
    # 检查权限
    if class_info["teacher_id"] != payload.get("sub"):
        raise HTTPException(status_code=403, detail="您不是该班级的教师")
    
    # 验证学生是否存在
    valid_students = []
    for student_id in student_ids:
        if student_id in mock_users and mock_users[student_id]["role"] == "student":
            valid_students.append(student_id)
        else:
            print(f"警告：学生 {student_id} 不存在或不是学生角色")
    
    # 添加学生（避免重复）
    existing_students = set(class_info["students"])
    new_students = [s for s in valid_students if s not in existing_students]
    class_info["students"].extend(new_students)
    
    # 保存更新
    save_class_info(class_info)
    
    return {
        "message": f"成功添加 {len(new_students)} 名学生",
        "added_students": new_students,
        "total_students": len(class_info["students"])
    }


@router.post("/{class_id}/assign-experiment")
async def assign_experiment(
    class_id: str,
    scenario_id: str = Body(...),
    mechanism_type: str = Body("uniform_price"),
    duration_hours: int = Body(24),
    description: str = Body(None),
    token: str = Depends(oauth2_scheme)
):
    """分配实验任务（教师专用）"""
    payload = decode_access_token(token)
    if not payload or payload.get("role") != "teacher":
        raise HTTPException(status_code=403, detail="只有教师可以分配实验")
    
    # 检查班级权限
    class_info = get_class_info(class_id)
    if not class_info or class_info["teacher_id"] != payload.get("sub"):
        raise HTTPException(status_code=403, detail="您不是该班级的教师")
    
    # 检查场景是否存在
    from mock_data.file_storage import get_scenario
    scenario = get_scenario(scenario_id)
    if not scenario:
        raise HTTPException(status_code=404, detail="场景不存在")
    
    # 创建实验任务
    assignment_id = f"assignment_{uuid.uuid4().hex[:8]}"
    start_time = datetime.now()
    end_time = start_time + timedelta(hours=duration_hours)
    
    assignment = ExperimentAssignment(
        assignment_id=assignment_id,
        class_id=class_id,
        scenario_id=scenario_id,
        mechanism_type=mechanism_type,
        start_time=start_time,
        end_time=end_time,
        status="active",
        description=description
    )
    
    # 保存任务
    save_experiment_assignment(assignment.dict())
    
    return {
        "message": "实验任务分配成功",
        "assignment_id": assignment_id,
        "assignment": assignment.dict()
    }


@router.get("/{class_id}/progress")
async def get_class_progress(
    class_id: str,
    assignment_id: str = None,
    token: str = Depends(oauth2_scheme)
):
    """获取班级进度（教师专用）"""
    payload = decode_access_token(token)
    if not payload or payload.get("role") != "teacher":
        raise HTTPException(status_code=403, detail="只有教师可以查看班级进度")
    
    # 检查班级权限
    class_info = get_class_info(class_id)
    if not class_info or class_info["teacher_id"] != payload.get("sub"):
        raise HTTPException(status_code=403, detail="您不是该班级的教师")
    
    # 获取实验任务
    assignments = get_experiment_assignments(class_id)
    if assignment_id:
        assignments = [a for a in assignments if a["assignment_id"] == assignment_id]
    
    # 计算进度
    progress_data = []
    for assignment in assignments:
        scenario_id = assignment["scenario_id"]
        students = class_info["students"]
        
        # 获取竞价数据
        from mock_data.file_storage import get_bids
        bid_data = get_bids(scenario_id)
        
        # 计算每个学生的进度
        for student_id in students:
            submitted = student_id in bid_data
            progress = StudentProgress(
                student_id=student_id,
                scenario_id=scenario_id,
                assignment_id=assignment["assignment_id"],
                submitted=submitted,
                submitted_at=bid_data.get(student_id, {}).get("submitted_at") if submitted else None
            )
            progress_data.append(progress.dict())
    
    return {
        "class_info": class_info,
        "assignments": assignments,
        "progress": progress_data,
        "summary": {
            "total_students": len(class_info["students"]),
            "total_assignments": len(assignments),
            "submission_rate": calculate_submission_rate(progress_data)
        }
    }


@router.get("/my-assignments")
async def get_my_assignments(token: str = Depends(oauth2_scheme)):
    """获取我的实验任务（学生专用）"""
    payload = decode_access_token(token)
    if not payload or payload.get("role") != "student":
        raise HTTPException(status_code=403, detail="只有学生可以查看实验任务")
    
    student_id = payload.get("sub")
    
    # 获取学生所在的班级
    all_classes = load_all_classes()
    my_classes = [cls for cls in all_classes if student_id in cls["students"]]
    
    # 获取所有实验任务
    all_assignments = []
    for class_info in my_classes:
        assignments = get_experiment_assignments(class_info["class_id"])
        for assignment in assignments:
            assignment["class_name"] = class_info["class_name"]
            all_assignments.append(assignment)
    
    return all_assignments


# 辅助函数
def save_class_info(class_info: Dict):
    """保存班级信息"""
    filename = "mock_data/classes.json"
    all_classes = load_all_classes()
    all_classes[class_info["class_id"]] = class_info
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(all_classes, f, ensure_ascii=False, indent=2, default=str)


def load_all_classes() -> Dict:
    """加载所有班级信息"""
    filename = "mock_data/classes.json"
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


def get_class_info(class_id: str) -> Dict:
    """获取班级信息"""
    all_classes = load_all_classes()
    return all_classes.get(class_id)


def save_experiment_assignment(assignment: Dict):
    """保存实验任务"""
    filename = "mock_data/assignments.json"
    all_assignments = load_all_assignments()
    all_assignments[assignment["assignment_id"]] = assignment
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(all_assignments, f, ensure_ascii=False, indent=2, default=str)


def load_all_assignments() -> Dict:
    """加载所有实验任务"""
    filename = "mock_data/assignments.json"
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


def get_experiment_assignments(class_id: str) -> List[Dict]:
    """获取班级的实验任务"""
    all_assignments = load_all_assignments()
    return [a for a in all_assignments.values() if a["class_id"] == class_id]


def calculate_submission_rate(progress_data: List[Dict]) -> float:
    """计算提交率"""
    if not progress_data:
        return 0.0
    
    submitted_count = sum(1 for p in progress_data if p["submitted"])
    return round(submitted_count / len(progress_data) * 100, 2) 