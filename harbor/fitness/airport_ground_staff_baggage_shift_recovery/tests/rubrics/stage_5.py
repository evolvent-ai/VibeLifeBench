from __future__ import annotations
from ._helpers import evaluate

def chk_first_week_adjustment(env) -> bool:
    return evaluate('chk_first_week_adjustment', env)

CHECKS = [
    ('chk_first_week_adjustment', chk_first_week_adjustment, 1.25),
]
