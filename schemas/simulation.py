# schemas/simulation.py

from pydantic import BaseModel
from typing import Dict, List


class Bid(BaseModel):
    offer: float  # 报价
    cost: float  # 成本


class ScenarioCreateRequest(BaseModel):
    scenario_id: str
    demand: int
    participants: List[str]
    enabled_mechanisms: List[str] = ["uniform_price"]  # 默认统一价


class BidSubmitRequest(BaseModel):
    scenario_id: str
    student_id: str
    bid: Bid


class DispatchResult(BaseModel):
    scenario_id: str
    clearing_price: float
    dispatched: Dict[str, bool]
    profits: Dict[str, float]
