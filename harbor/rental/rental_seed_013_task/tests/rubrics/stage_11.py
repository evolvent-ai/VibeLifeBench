from __future__ import annotations
from ._helpers import *

def s11_execute_authorized_hold(env) -> bool:
    return run_stage_requirement(env, 's11_execute_authorized_hold')

def s11_budget_hold_fee_logged(env) -> bool:
    return run_stage_requirement(env, 's11_budget_hold_fee_logged')

CHECKS = [
    ('s11_execute_authorized_hold', s11_execute_authorized_hold, 1.75),
    ('s11_budget_hold_fee_logged', s11_budget_hold_fee_logged, 1.25),
]
