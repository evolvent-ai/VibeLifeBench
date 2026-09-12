from __future__ import annotations
from ._helpers import _check

def chk_s11_sleep_debt_downgrade(env) -> bool:
    return _check('chk_s11_sleep_debt_downgrade', env)

def chk_s11_recovery_priority(env) -> bool:
    return _check('chk_s11_recovery_priority', env)

CHECKS = [
    ('chk_s11_sleep_debt_downgrade', chk_s11_sleep_debt_downgrade, 2.0),
    ('chk_s11_recovery_priority', chk_s11_recovery_priority, 1.5),
]
