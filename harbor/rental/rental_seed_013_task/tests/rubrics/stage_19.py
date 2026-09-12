from __future__ import annotations
from ._helpers import *

def s19_refresh_long204_night_risk(env) -> bool:
    return run_stage_requirement(env, 's19_refresh_long204_night_risk')

def s19_downgrade_long204_conditionally(env) -> bool:
    return run_stage_requirement(env, 's19_downgrade_long204_conditionally')

CHECKS = [
    ('s19_refresh_long204_night_risk', s19_refresh_long204_night_risk, 1.75),
    ('s19_downgrade_long204_conditionally', s19_downgrade_long204_conditionally, 1.25),
]
