# services/market_clear/two_stage_market.py

from schemas.simulation import DispatchResult
from typing import Dict


def clear_market_two_stage(scenario: Dict, bid_data: Dict[str, dict]) -> DispatchResult:
    demand_da = scenario.get("demand_DA", scenario["demand"])  # 日前需求
    demand_rt = scenario.get("demand_RT", scenario["demand"])  # 实时需求

    # Step 1: 日前市场出清（DA）
    sorted_da = sorted(bid_data.items(), key=lambda x: x[1].get("offer_DA", x[1]["offer"]))
    winners_da = sorted_da[:demand_da]
    price_da = winners_da[-1][1].get("offer_DA", winners_da[-1][1]["offer"])

    # Step 2: 实时市场补差值（RT）
    sorted_rt = sorted(bid_data.items(), key=lambda x: x[1].get("offer_RT", x[1]["offer"]))
    winners_rt = sorted_rt[:demand_rt]
    price_rt = winners_rt[-1][1].get("offer_RT", winners_rt[-1][1]["offer"])

    dispatched = {}
    profits = {}

    for student_id, bid in bid_data.items():
        cost = bid.get("cost", 0)
        fixed_cost = bid.get("fixed_cost", 0)

        offer_da = bid.get("offer_DA", bid["offer"])
        offer_rt = bid.get("offer_RT", bid["offer"])

        in_da = student_id in dict(winners_da)
        in_rt = student_id in dict(winners_rt)

        dispatched[student_id] = in_da or in_rt

        profit = 0.0
        if in_da:
            profit += price_da - cost - fixed_cost
        if in_rt and not in_da:
            profit += price_rt - cost - fixed_cost  # 只补实时差额

        profits[student_id] = round(profit, 2)

    return DispatchResult(
        scenario_id=scenario["scenario_id"],
        clearing_price=price_rt,  # 以 RT 市场价格为最终展示价
        dispatched=dispatched,
        profits=profits
    )