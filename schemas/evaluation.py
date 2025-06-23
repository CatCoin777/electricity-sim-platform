# schemas/evaluation.py

from pydantic import BaseModel
from typing import Dict, List, Optional
from datetime import datetime


class EvaluationCriteria(BaseModel):
    """评估标准"""
    scenario_id: str
    mechanism_type: str
    target_price: Optional[float] = None  # 目标出清价格
    target_profit: Optional[float] = None  # 目标利润
    price_weight: float = 0.5  # 价格权重
    profit_weight: float = 0.5  # 利润权重


class StudentScore(BaseModel):
    """学生成绩"""
    student_id: str
    scenario_id: str
    mechanism_type: str
    submitted_bid: Dict  # 提交的竞价
    actual_result: Dict  # 实际结果
    price_score: float  # 价格得分
    profit_score: float  # 利润得分
    total_score: float  # 总分
    rank: int  # 排名
    submitted_at: datetime


class ClassEvaluation(BaseModel):
    """班级评估"""
    class_id: str
    scenario_id: str
    mechanism_type: str
    evaluation_criteria: EvaluationCriteria
    student_scores: List[StudentScore]
    class_average: float
    class_rankings: Dict[str, int]  # 学生ID -> 排名


class ExperimentReport(BaseModel):
    """实验报告"""
    scenario_id: str
    mechanism_type: str
    total_participants: int
    submitted_count: int
    submission_rate: float
    average_score: float
    score_distribution: Dict[str, int]  # 分数段 -> 人数
    top_performers: List[str]  # 前几名学生ID
    analysis_summary: str 