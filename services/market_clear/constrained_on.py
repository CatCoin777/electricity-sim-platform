# services/market_clear/constrained_on.py

from schemas.simulation import DispatchResult
from typing import Dict
from collections import defaultdict


def clear_market_constrained_on(scenario: Dict, bid_data: Dict[str, dict]) -> DispatchResult:
    demand = scenario["demand"]
    must_run = scenario.get("must_run", [])  # 强制运行者 ID 列表

    # Step 1: 正常按报价排序调度
    sorted_bids = sorted(bid_data.items(), key=lambda x: x[1]["offer"])
    winners = sorted_bids[:demand]
    clearing_price = winners[-1][1]["offer"]

    dispatched = {}
    profits = {}

    winners_dict = dict(winners)

    for student_id, bid in bid_data.items():
        cost = bid.get("cost", 0)
        fixed_cost = bid.get("fixed_cost", 0)

        if student_id in winners_dict:
            dispatched[student_id] = True
            profit = clearing_price - cost - fixed_cost
            profits[student_id] = round(profit, 2)
        elif student_id in must_run:
            dispatched[student_id] = True
            compensation = -cost - fixed_cost
            profits[student_id] = round(compensation, 2)  # 补偿为负成本（系统支付）
        else:
            dispatched[student_id] = False
            profits[student_id] = 0.0

    return DispatchResult(
        scenario_id=scenario["scenario_id"],
        clearing_price=clearing_price,
        dispatched=dispatched,
        profits=profits
    )
