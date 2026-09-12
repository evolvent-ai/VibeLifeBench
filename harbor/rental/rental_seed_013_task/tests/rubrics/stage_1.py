from __future__ import annotations
from ._helpers import *

def s1_verify_onboarding_office_a(env) -> bool:
    return run_stage_requirement(env, 's1_verify_onboarding_office_a')

def s1_subscribe_office_recheck(env) -> bool:
    return run_stage_requirement(env, 's1_subscribe_office_recheck')

CHECKS = [
    ('s1_verify_onboarding_office_a', s1_verify_onboarding_office_a, 1.5),
    ('s1_subscribe_office_recheck', s1_subscribe_office_recheck, 1.25),
]
