from __future__ import annotations
from ._helpers import evaluate

def chk_thunderstorm_alt_plan(env) -> bool:
    return evaluate('chk_thunderstorm_alt_plan', env)

CHECKS = [
    ('chk_thunderstorm_alt_plan', chk_thunderstorm_alt_plan, 2.0),
]
