# services/market_clear/fixed_cost_pay_as_bid.py

from schemas.simulation import DispatchResult
from typing import Dict


def clear_market_fixed_pay_as_bid(scenario: Dict, bid_data: Dict[str, dict]) -> DispatchResult:
    demand = scenario["demand"]

    # Step 1: 按报价从低到高排序
    sorted_bids = sorted(bid_data.items(), key=lambda x: x[1]["offer"])
    winners = sorted_bids[:demand]

    if len(winners) < demand:
        raise ValueError("Not enough bids to satisfy demand")

    # Step 2: 不统一定价，每人按自己报价收入
    dispatched = {}
    profits = {}
    clearing_price = 0  # 统一价为0（或空），表示是 pay-as-bid 模式

    for student, bid in bid_data.items():
        offer = bid["offer"]
        cost = bid.get("cost", 0)
        fixed_cost = bid.get("fixed_cost", 0)

        if student in dict(winners):
            dispatched[student] = True
            profit = offer - cost - fixed_cost
            profits[student] = round(profit, 2)
        else:
            dispatched[student] = False
            profits[student] = 0.0

    return DispatchResult(
        scenario_id=scenario["scenario_id"],
        clearing_price=clearing_price,
        dispatched=dispatched,
        profits=profits
    )
