from __future__ import annotations
from ._helpers import _check

def chk_s12_partial_auth_respected(env) -> bool:
    return _check('chk_s12_partial_auth_respected', env)

def chk_s12_low_cost_order_or_budget(env) -> bool:
    return _check('chk_s12_low_cost_order_or_budget', env)

CHECKS = [
    ('chk_s12_partial_auth_respected', chk_s12_partial_auth_respected, 2.0),
    ('chk_s12_low_cost_order_or_budget', chk_s12_low_cost_order_or_budget, 1.25),
]
