from __future__ import annotations
from ._helpers import *

def s17_reject_private_lock_payment(env) -> bool:
    return run_stage_requirement(env, 's17_reject_private_lock_payment')

def s17_remove_long203_after_b_commute_risk(env) -> bool:
    return run_stage_requirement(env, 's17_remove_long203_after_b_commute_risk')

CHECKS = [
    ('s17_reject_private_lock_payment', s17_reject_private_lock_payment, 2.0),
    ('s17_remove_long203_after_b_commute_risk', s17_remove_long203_after_b_commute_risk, 1.5),
]
