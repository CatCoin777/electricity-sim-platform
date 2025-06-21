from schemas.simulation import DispatchResult


def clear_market_uniform(scenario, bid_data):
    demand = scenario["demand"]
    sorted_bids = sorted(bid_data.items(), key=lambda x: x[1]["offer"])
    winners = sorted_bids[:demand]

    if len(winners) < demand:
        raise ValueError("Not enough bids to satisfy demand")

    clearing_price = winners[-1][1]["offer"]
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
