from schemas.simulation import DispatchResult
from fastapi import HTTPException


def clear_market_uniform(scenario, bid_data):
    demand = scenario["demand"]
    sorted_bids = sorted(bid_data.items(), key=lambda x: x[1].get('offer', x[1].get('price')))
    winners = sorted_bids[:demand]

    if len(sorted_bids) < demand:
        raise HTTPException(status_code=400, detail=f"Not enough bids to satisfy demand. Demand={demand}, bids={len(sorted_bids)}")

    clearing_price = winners[-1][1].get('offer', winners[-1][1].get('price'))
    dispatched = {}
    profits = {}

    for student, bid in bid_data.items():
        if student in dict(winners):
            dispatched[student] = True
            profits[student] = round(clearing_price - bid["cost"], 2)
        else:
            dispatched[student] = False
            profits[student] = 0.0

    return DispatchResult(
        scenario_id=scenario["scenario_id"],
        clearing_price=clearing_price,
        dispatched=dispatched,
        profits=profits
    )
