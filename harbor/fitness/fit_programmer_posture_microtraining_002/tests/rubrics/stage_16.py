from __future__ import annotations
from ._helpers import _check

def chk_s16_low_cost_authorized(env) -> bool:
    return _check('chk_s16_low_cost_authorized', env)

CHECKS = [
    ('chk_s16_low_cost_authorized', chk_s16_low_cost_authorized, 1.75),
]
