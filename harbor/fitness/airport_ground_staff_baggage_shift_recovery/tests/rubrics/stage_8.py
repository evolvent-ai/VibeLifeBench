from __future__ import annotations
from ._helpers import evaluate

def chk_no_hiit_after_night(env) -> bool:
    return evaluate('chk_no_hiit_after_night', env)

CHECKS = [
    ('chk_no_hiit_after_night', chk_no_hiit_after_night, 2.0),
]
