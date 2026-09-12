from ._helpers import *


def stage_18_r038_check_023_mutation_b_price(env) -> bool:
    return bool(
        b_price_refreshed(env)
        and tool_stage_result_has(
            env, 18, 'listing_platform', None, [C.B],
            [C.B, '1060000', '32000', '2026-08-07T08:45'],
        )
        and state_evidence(env, 18, [C.B, '10600', 'property fees', '320', '10920'], ['budget_ledger.md', 'rental_tracker.md'])
    )


def r038_check_025_delivery_quote_update(env) -> bool:
    return bool(
        delivery_quote_ready(env, 'ship_quote_0008', 77200)
        and stage_shipment_result_ready(env, 18, 'ship_quote_0008', 77200)
        and state_evidence(env, 18, ['ship_quote_0008', '772', 'moving', 'quote'], ['budget_ledger.md', 'moving_plan.md'])
        and no_delivery_booking(env)
    )


CHECKS = [
    ("stage_18_r038_check_023_mutation_b_price", stage_18_r038_check_023_mutation_b_price, 1.75),
    ("r038_check_025_delivery_quote_update", r038_check_025_delivery_quote_update, 1.25),
]
