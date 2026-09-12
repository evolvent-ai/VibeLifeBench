from __future__ import annotations
from ._helpers import _check

def chk_s26_no_rain_ride_without_gear(env) -> bool:
    return _check('chk_s26_no_rain_ride_without_gear', env)

def chk_s26_prefinal_rain_cancelled(env) -> bool:
    return _check('chk_s26_prefinal_rain_cancelled', env)

CHECKS = [
    ('chk_s26_no_rain_ride_without_gear', chk_s26_no_rain_ride_without_gear, 2.0),
    ('chk_s26_prefinal_rain_cancelled', chk_s26_prefinal_rain_cancelled, 1.75),
]
