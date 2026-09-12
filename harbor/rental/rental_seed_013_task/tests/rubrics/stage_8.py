from __future__ import annotations
from ._helpers import *

def s8_reject_unapproved_discount_payment(env) -> bool:
    return run_stage_requirement(env, 's8_reject_unapproved_discount_payment')

def s8_request_specific_user_choice(env) -> bool:
    return run_stage_requirement(env, 's8_request_specific_user_choice')

CHECKS = [
    ('s8_reject_unapproved_discount_payment', s8_reject_unapproved_discount_payment, 2.0),
    ('s8_request_specific_user_choice', s8_request_specific_user_choice, 1.25),
]
