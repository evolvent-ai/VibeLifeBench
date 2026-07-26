from __future__ import annotations
from ._helpers import evaluate

def chk_s25_final_refresh(env) -> bool:
    return evaluate('chk_s25_final_refresh', env)

CHECKS = [
    ('chk_s25_final_refresh', chk_s25_final_refresh, 1.25),
]
