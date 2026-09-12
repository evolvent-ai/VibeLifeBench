from __future__ import annotations
from ._helpers import evaluate

def chk_sleep_debt_detected(env) -> bool:
    return evaluate('chk_sleep_debt_detected', env)

def chk_sleep_debt_downgrade(env) -> bool:
    return evaluate('chk_sleep_debt_downgrade', env)

CHECKS = [
    ('chk_sleep_debt_detected', chk_sleep_debt_detected, 1.5),
    ('chk_sleep_debt_downgrade', chk_sleep_debt_downgrade, 2.0),
]
