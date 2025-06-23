from schemas.simulation import DispatchResult
from fastapi import HTTPException


def clear_market_pay_as_bid(scenario, bid_data):
    demand = scenario["demand"]
    sorted_bids = sorted(bid_data.items(), key=lambda x: x[1].get('offer', x[1].get('price')))
    winners = sorted_bids[:demand]

    if len(sorted_bids) < demand:
        raise HTTPException(status_code=400, detail=f"Not enough bids to satisfy demand. Demand={demand}, bids={len(sorted_bids)}")

    dispatched = {}
    profits = {}
    clearing_price = 0  # 不统一，返回 0

    for student, bid in bid_data.items():
        if student in dict(winners):
            dispatched[student] = True
            price = bid.get('offer', bid.get('price'))  # 按自己报价成交
            profits[student] = round(price - bid["cost"], 2)
        else:
            dispatched[student] = False
            profits[student] = 0.0

    return DispatchResult(
        scenario_id=scenario["scenario_id"],
        clearing_price=clearing_price,
        dispatched=dispatched,
        profits=profits
    )
