from __future__ import annotations
from ._helpers import _check

def chk_s06_first_ride_progression(env) -> bool:
    return _check('chk_s06_first_ride_progression', env)

CHECKS = [
    ('chk_s06_first_ride_progression', chk_s06_first_ride_progression, 1.5),
]
