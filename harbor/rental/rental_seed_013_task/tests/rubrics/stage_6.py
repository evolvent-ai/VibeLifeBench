from __future__ import annotations
from ._helpers import *

def s6_refresh_short_101_delay(env) -> bool:
    return run_stage_requirement(env, 's6_refresh_short_101_delay')

def s6_recompute_short_budget(env) -> bool:
    return run_stage_requirement(env, 's6_recompute_short_budget')

CHECKS = [
    ('s6_refresh_short_101_delay', s6_refresh_short_101_delay, 1.75),
    ('s6_recompute_short_budget', s6_recompute_short_budget, 1.25),
]
