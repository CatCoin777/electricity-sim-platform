# routers/simulation.py

from fastapi import APIRouter, HTTPException, Query, Depends, Body
from fastapi.security import OAuth2PasswordBearer
from schemas.simulation import DispatchResult, BidSubmitRequest
from mock_data.file_storage import get_scenario, get_bids, save_bid
from services.market_clear.constrained_on import clear_market_constrained_on
from services.market_clear.fixed_cost_pay_as_bid import clear_market_fixed_pay_as_bid
from services.market_clear.fixed_cost_uniform import clear_market_fixed_uniform
from services.market_clear.risk_adjusted_uniform import clear_market_risk_adjusted_uniform
from services.market_clear.two_stage_market import clear_market_two_stage
from services.market_clear.uniform_price import clear_market_uniform
from services.market_clear.pay_as_bid import clear_market_pay_as_bid
from services.market_clear.zone_limit_uniform import clear_market_zone_uniform
from security import decode_access_token
from routers.classes import get_class_info, get_experiment_assignments
from typing import List, Dict, Any

router = APIRouter(prefix="/api/simulation", tags=["Simulation"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


@router.post("/bid")
def submit_bid(req: BidSubmitRequest, token: str = Depends(oauth2_scheme)):
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    student_id = payload.get("sub")
    if student_id != req.student_id:
        raise HTTPException(status_code=403, detail="You can only submit bids for yourself")
    
    scenario = get_scenario(req.scenario_id)
    if not scenario:
        raise HTTPException(status_code=404, detail="Scenario not found")
    
    # Check if user can participate in this scenario
    if not can_user_participate(student_id, scenario):
        raise HTTPException(status_code=403, detail="You are not eligible to participate in this scenario")
    
    save_bid(req.scenario_id, req.student_id, req.bid.dict())
    return {"message": "Bid submitted successfully"}


@router.get("/result/{scenario_id}", response_model=DispatchResult)
def get_result(scenario_id: str, type: str = Query("uniform_price"), token: str = Depends(oauth2_scheme)):
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    scenario = get_scenario(scenario_id)
    if not scenario:
        raise HTTPException(status_code=404, detail="Scenario not found")

    bid_data = get_bids(scenario_id)

    if type not in scenario.get("enabled_mechanisms", []):
        raise HTTPException(status_code=400, detail=f"Mechanism '{type}' not enabled for this scenario")

    if type == "uniform_price":
        return clear_market_uniform(scenario, bid_data)
    elif type == "pay_as_bid":
        return clear_market_pay_as_bid(scenario, bid_data)
    elif type == "fixed_cost_uniform":
        return clear_market_fixed_uniform(scenario, bid_data)
    elif type == "fixed_cost_pay_as_bid":
        return clear_market_fixed_pay_as_bid(scenario, bid_data)
    elif type == "zone_limit_uniform":
        return clear_market_zone_uniform(scenario, bid_data)
    elif type == "constrained_on":
        return clear_market_constrained_on(scenario, bid_data)
    elif type == "risk_adjusted_uniform":
        return clear_market_risk_adjusted_uniform(scenario, bid_data)
    elif type == "two_stage":
        return clear_market_two_stage(scenario, bid_data)
    else:
        raise HTTPException(status_code=400, detail="Unknown market mechanism")


@router.get("/available-scenarios")
def get_available_scenarios(token: str = Depends(oauth2_scheme)):
    """Get scenarios available for the current user"""
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    user_id = payload.get("sub")
    user_role = payload.get("role")
    
    # Get all scenarios
    from mock_data.file_storage import list_scenarios
    all_scenarios = list_scenarios()
    
    available_scenarios = []
    
    for scenario_id, scenario in all_scenarios.items():
        if can_user_participate(user_id, scenario):
            available_scenarios.append(scenario)
    
    return available_scenarios


def can_user_participate(user_id: str, scenario: dict) -> bool:
    """Check if user can participate in the scenario"""
    # If scenario is open to all users
    if scenario.get("is_open", False):
        return True
    
    # If scenario is restricted to specific participants
    if user_id in scenario.get("participants", []):
        return True
    
    # If scenario is associated with a class
    class_id = scenario.get("class_id")
    if class_id:
        class_info = get_class_info(class_id)
        if class_info and user_id in class_info.get("students", []):
            return True
    
    return False