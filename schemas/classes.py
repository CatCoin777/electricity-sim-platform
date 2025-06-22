# schemas/classes.py

from pydantic import BaseModel
from typing import List, Dict, Optional
from datetime import datetime


class ClassInfo(BaseModel):
    """班级信息"""
    class_id: str
    class_name: str
    teacher_id: str
    students: List[str]  # 学生ID列表
    created_at: datetime
    description: Optional[str] = None


class ClassMember(BaseModel):
    """班级成员"""
    user_id: str
    username: str
    full_name: str
    role: str  # student 或 teacher
    join_date: datetime


class ExperimentAssignment(BaseModel):
    """实验任务分配"""
    assignment_id: str
    class_id: str
    scenario_id: str
    mechanism_type: str
    start_time: datetime
    end_time: datetime
    status: str  # active, completed, expired
    description: Optional[str] = None


class StudentProgress(BaseModel):
    """学生进度"""
    student_id: str
    scenario_id: str
    assignment_id: str
    submitted: bool
    submitted_at: Optional[datetime] = None
    score: Optional[float] = None
    rank: Optional[int] = None 