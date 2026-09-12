from __future__ import annotations
from ._helpers import evaluate

def chk_final_week_shift_split(env) -> bool:
    return evaluate('chk_final_week_shift_split', env)

CHECKS = [
    ('chk_final_week_shift_split', chk_final_week_shift_split, 1.5),
]
