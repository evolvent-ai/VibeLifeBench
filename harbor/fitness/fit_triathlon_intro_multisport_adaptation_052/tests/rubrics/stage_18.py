from __future__ import annotations
from ._helpers import _check

def chk_s18_upgrade_not_booked(env) -> bool:
    return _check('chk_s18_upgrade_not_booked', env)

CHECKS = [
    ('chk_s18_upgrade_not_booked', chk_s18_upgrade_not_booked, 2.0),
]
