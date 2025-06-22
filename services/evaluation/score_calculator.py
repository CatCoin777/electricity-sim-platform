# services/evaluation/score_calculator.py

from schemas.evaluation import EvaluationCriteria, StudentScore
from schemas.simulation import DispatchResult
from typing import Dict, List
import math


def calculate_student_score(
    student_id: str,
    scenario_id: str,
    mechanism_type: str,
    submitted_bid: Dict,
    actual_result: DispatchResult,
    criteria: EvaluationCriteria
) -> StudentScore:
    """计算学生成绩"""
    
    # 获取学生的实际结果
    dispatched = actual_result.dispatched.get(student_id, False)
    profit = actual_result.profits.get(student_id, 0.0)
    clearing_price = actual_result.clearing_price
    
    # 计算价格得分
    price_score = calculate_price_score(
        submitted_bid.get("offer", 0),
        clearing_price,
        criteria.target_price,
        criteria.price_weight
    )
    
    # 计算利润得分
    profit_score = calculate_profit_score(
        profit,
        criteria.target_profit,
        criteria.profit_weight
    )
    
    # 计算总分
    total_score = price_score + profit_score
    
    return StudentScore(
        student_id=student_id,
        scenario_id=scenario_id,
        mechanism_type=mechanism_type,
        submitted_bid=submitted_bid,
        actual_result=actual_result.dict(),
        price_score=price_score,
        profit_score=profit_score,
        total_score=total_score,
        rank=0,  # 稍后计算排名
        submitted_at=actual_result.submitted_at if hasattr(actual_result, 'submitted_at') else None
    )


def calculate_price_score(
    submitted_price: float,
    clearing_price: float,
    target_price: float = None,
    weight: float = 0.5
) -> float:
    """计算价格得分"""
    
    if target_price is None:
        # 如果没有目标价格，基于与出清价格的接近程度评分
        if clearing_price == 0:  # Pay-as-bid 机制
            return weight * 50  # 基础分
        
        price_diff = abs(submitted_price - clearing_price)
        max_diff = clearing_price * 0.5  # 最大允许偏差50%
        
        if price_diff <= max_diff:
            score = weight * (100 - (price_diff / max_diff) * 50)
        else:
            score = weight * 25  # 最低分
        
        return max(0, score)
    else:
        # 基于与目标价格的接近程度评分
        price_diff = abs(submitted_price - target_price)
        max_diff = target_price * 0.3  # 最大允许偏差30%
        
        if price_diff <= max_diff:
            score = weight * (100 - (price_diff / max_diff) * 50)
        else:
            score = weight * 25
        
        return max(0, score)


def calculate_profit_score(
    actual_profit: float,
    target_profit: float = None,
    weight: float = 0.5
) -> float:
    """计算利润得分"""
    
    if target_profit is None:
        # 如果没有目标利润，基于利润的正负和大小评分
        if actual_profit > 0:
            # 正利润，基于利润大小评分
            score = weight * min(100, actual_profit * 10)  # 每1元利润得10分，最高100分
        elif actual_profit == 0:
            # 零利润，基础分
            score = weight * 30
        else:
            # 负利润，扣分
            score = weight * max(0, 30 + actual_profit * 5)  # 每1元亏损扣5分
        
        return max(0, score)
    else:
        # 基于与目标利润的接近程度评分
        profit_diff = abs(actual_profit - target_profit)
        max_diff = abs(target_profit) * 0.5  # 最大允许偏差50%
        
        if profit_diff <= max_diff:
            score = weight * (100 - (profit_diff / max_diff) * 50)
        else:
            score = weight * 25
        
        return max(0, score)


def calculate_class_rankings(scores: List[StudentScore]) -> Dict[str, int]:
    """计算班级排名"""
    # 按总分降序排序
    sorted_scores = sorted(scores, key=lambda x: x.total_score, reverse=True)
    
    rankings = {}
    current_rank = 1
    current_score = None
    
    for i, score in enumerate(sorted_scores):
        if current_score != score.total_score:
            current_rank = i + 1
            current_score = score.total_score
        
        rankings[score.student_id] = current_rank
    
    return rankings


def generate_score_distribution(scores: List[StudentScore]) -> Dict[str, int]:
    """生成分数分布"""
    distribution = {
        "优秀 (90-100)": 0,
        "良好 (80-89)": 0,
        "中等 (70-79)": 0,
        "及格 (60-69)": 0,
        "不及格 (0-59)": 0
    }
    
    for score in scores:
        total_score = score.total_score
        if total_score >= 90:
            distribution["优秀 (90-100)"] += 1
        elif total_score >= 80:
            distribution["良好 (80-89)"] += 1
        elif total_score >= 70:
            distribution["中等 (70-79)"] += 1
        elif total_score >= 60:
            distribution["及格 (60-69)"] += 1
        else:
            distribution["不及格 (0-59)"] += 1
    
    return distribution


def calculate_class_average(scores: List[StudentScore]) -> float:
    """计算班级平均分"""
    if not scores:
        return 0.0
    
    total_score = sum(score.total_score for score in scores)
    return round(total_score / len(scores), 2) 