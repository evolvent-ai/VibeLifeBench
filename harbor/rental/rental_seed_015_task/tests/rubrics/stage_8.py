from __future__ import annotations
from ._helpers import *

def s8_elevator_mutation_recovery(env) -> bool:
    ok = stage_ok(env, 8, 's8')
    return ok and listing_a_elevator_mutated(env) and review_has(env, "mer_a", ["elevator", "maintenance"])

def s8_listing_a_downgraded(env) -> bool:
    ok = stage_ok(env, 8, 's8')
    return ok and listing_a_elevator_mutated(env) and tool_stage(env, 8, NOTION, None, [])

CHECKS = [
    ('s8_elevator_mutation_recovery', s8_elevator_mutation_recovery, 1.75),
    ('s8_listing_a_downgraded', s8_listing_a_downgraded, 1.5),
]
