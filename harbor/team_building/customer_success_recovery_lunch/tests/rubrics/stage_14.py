from __future__ import annotations
from ._helpers import *

def s14_two_plan_no_payment(env) -> bool:
    return any_write(env, 14) and state_has(env, 14, [['two plans'], ['budget'], ['not pay'], ['confirmation']])

CHECKS = [
    ('s14_two_plan_no_payment', s14_two_plan_no_payment, 1.5),
]
