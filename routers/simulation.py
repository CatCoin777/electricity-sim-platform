# routers/simulation.py

from fastapi import APIRouter, HTTPException, Query
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

router = APIRouter(prefix="/simulation", tags=["Simulation"])


@router.post("/bid")
def submit_bid(req: BidSubmitRequest):
    scenario = get_scenario(req.scenario_id)
    if not scenario:
        raise HTTPException(status_code=404, detail="Scenario not found")
    if req.student_id not in scenario["participants"]:
        raise HTTPException(status_code=403, detail="You are not a participant")
    save_bid(req.scenario_id, req.student_id, req.bid.dict())
    return {"message": "Bid submitted"}


@router.get("/result/{scenario_id}", response_model=DispatchResult)
def get_result(scenario_id: str, type: str = Query("uniform_price")):
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