# services/market_clear/zone_limit_uniform.py

from schemas.simulation import DispatchResult
from typing import Dict
from collections import defaultdict


def clear_market_zone_uniform(scenario: Dict, bid_data: Dict[str, dict]) -> DispatchResult:
    demand = scenario["demand"]
    zone_limits = scenario.get("zone_limits", {})  # e.g., {"West": 2, "East": 2}

    # 按报价升序排列
    sorted_bids = sorted(bid_data.items(), key=lambda x: x[1]["offer"])
    winners = []
    zone_count = defaultdict(int)
    total_dispatched = 0

    # 分区限制调度
    for student_id, bid in sorted_bids:
        zone = bid.get("zone")
        if zone is None:
            continue

        if zone_count[zone] < zone_limits.get(zone, demand):
            winners.append((student_id, bid))
            zone_count[zone] += 1
            total_dispatched += 1

        if total_dispatched >= demand:
            break

    if total_dispatched < demand:
        raise ValueError("Unable to fulfill demand under zone constraints")

    clearing_price = winners[-1][1]["offer"]
    dispatched = {}
    profits = {}

    for student_id, bid in bid_data.items():
        cost = bid.get("cost", 0)
        if student_id in dict(winners):
            dispatched[student_id] = True
            profits[student_id] = round(clearing_price - cost, 2)
        else:
            dispatched[student_id] = False
            profits[student_id] = 0.0

    return DispatchResult(
        scenario_id=scenario["scenario_id"],
        clearing_price=clearing_price,
        dispatched=dispatched,
        profits=profits
    )
