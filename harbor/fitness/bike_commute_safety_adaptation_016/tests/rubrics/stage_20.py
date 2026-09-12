from __future__ import annotations
from ._helpers import _check

def chk_s20_sleep_debt_downgrade(env) -> bool:
    return _check('chk_s20_sleep_debt_downgrade', env)

CHECKS = [
    ('chk_s20_sleep_debt_downgrade', chk_s20_sleep_debt_downgrade, 2.0),
]
