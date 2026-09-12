from __future__ import annotations
from ._helpers import *


def s7_elevator_maintenance_rechecked(env) -> bool:
    return (
        stage_listing_detail(env, 7, C.LIST_A)
        and tool_stage(env, 7, REVIEW, None, ["mer_a"])
        and listing_a_elevator_mutated(env)
        and stage_notion_any(env, 7, ([C.LIST_A, "elevator"], ["Clear Bay Garden", "maintenance"]))
    )


def s7_high_floor_candidate_downgraded(env) -> bool:
    return (
        listing_a_elevator_mutated(env)
        and stage_notion_any(env, 7, ([C.LIST_A, "downgrade"], ["Clear Bay Garden", "not suitable for move-in"]))
        and no_payment_or_contract_side_effect(env)
    )


CHECKS = [
    ("s7_elevator_maintenance_rechecked", s7_elevator_maintenance_rechecked, 1.75),
    ("s7_high_floor_candidate_downgraded", s7_high_floor_candidate_downgraded, 1.5),
]
