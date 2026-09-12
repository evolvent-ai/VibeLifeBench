from __future__ import annotations
from ._helpers import evaluate

def chk_shift_aware_schedule(env) -> bool:
    return evaluate('chk_shift_aware_schedule', env)

CHECKS = [
    ('chk_shift_aware_schedule', chk_shift_aware_schedule, 1.5),
]
