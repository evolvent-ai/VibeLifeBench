from __future__ import annotations
from ._helpers import _check

def chk_s10_sleep_downgrade(env) -> bool:
    return _check('chk_s10_sleep_downgrade', env)

CHECKS = [
    ('chk_s10_sleep_downgrade', chk_s10_sleep_downgrade, 2),
]
