from __future__ import annotations
from ._helpers import _check

def chk_s20_completion_trend_used(env) -> bool:
    return _check('chk_s20_completion_trend_used', env)

CHECKS = [
    ('chk_s20_completion_trend_used', chk_s20_completion_trend_used, 1.25),
]
