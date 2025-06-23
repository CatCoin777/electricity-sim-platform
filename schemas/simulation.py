# schemas/simulation.py

from pydantic import BaseModel, validator
from typing import Dict, List, Optional


class Bid(BaseModel):
    offer: float  # 报价
    cost: float  # 成本
    fixed_cost: Optional[float] = 0.0  # 新增字段，默认 0


class ScenarioCreateRequest(BaseModel):
    scenario_id: str
    demand: int
    participants: List[str]
    enabled_mechanisms: List[str] = ["uniform_price"]  # 默认统一价
    is_open: bool = False  # 是否开放给所有用户
    class_id: Optional[str] = None  # 关联的班级ID

    @validator('demand')
    def validate_demand(cls, v):
        if v < 1:
            raise ValueError('Demand must be at least 1')
        return v


class BidSubmitRequest(BaseModel):
    scenario_id: str
    student_id: str
    bid: Bid


class DispatchResult(BaseModel):
    scenario_id: str
    clearing_price: float
    dispatched: Dict[str, bool]
    profits: Dict[str, float]
