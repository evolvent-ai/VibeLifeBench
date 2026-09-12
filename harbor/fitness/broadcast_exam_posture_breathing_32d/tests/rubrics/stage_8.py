from __future__ import annotations
from ._helpers import evaluate

def chk_s08_sleep_fatigue_detected(env) -> bool:
    return evaluate('chk_s08_sleep_fatigue_detected', env)

CHECKS = [
    ('chk_s08_sleep_fatigue_detected', chk_s08_sleep_fatigue_detected, 2.0),
]
