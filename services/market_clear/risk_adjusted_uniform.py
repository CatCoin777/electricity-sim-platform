# services/market_clear/risk_adjusted_uniform.py

from schemas.simulation import DispatchResult
from typing import Dict


def clear_market_risk_adjusted_uniform(scenario: Dict, bid_data: Dict[str, dict]) -> DispatchResult:
    demand = scenario["demand"]

    # 使用期望报价 = offer / probability
    def expected_offer(bid):
        prob = bid.get("probability", 1.0)
        return bid["offer"] / prob if prob > 0 else float("inf")

    sorted_bids = sorted(bid_data.items(), key=lambda x: expected_offer(x[1]))
    winners = sorted_bids[:demand]

    if len(winners) < demand:
        raise ValueError("Not enough bids to satisfy demand")

    clearing_price = winners[-1][1]["offer"]
    dispatched = {}
    profits = {}

    for student_id, bid in bid_data.items():
        cost = bid.get("cost", 0)
        risk_cost = bid.get("risk_cost", 0)
        prob = bid.get("probability", 1.0)

        if student_id in dict(winners):
            dispatched[student_id] = True
            profit = clearing_price - cost - risk_cost * (1 - prob)
            profits[student_id] = round(profit, 2)
        else:
            dispatched[student_id] = False
            profits[student_id] = 0.0

    return DispatchResult(
        scenario_id=scenario["scenario_id"],
        clearing_price=clearing_price,
        dispatched=dispatched,
        profits=profits
    )
