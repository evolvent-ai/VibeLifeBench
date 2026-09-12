from __future__ import annotations
from ._helpers import _check

def chk_s10_rain_detected(env) -> bool:
    return _check('chk_s10_rain_detected', env)

def chk_s10_outdoor_replaced(env) -> bool:
    return _check('chk_s10_outdoor_replaced', env)

def chk_s10_weather_logged(env) -> bool:
    return _check('chk_s10_weather_logged', env)

CHECKS = [
    ('chk_s10_rain_detected', chk_s10_rain_detected, 1.5),
    ('chk_s10_outdoor_replaced', chk_s10_outdoor_replaced, 2.0),
    ('chk_s10_weather_logged', chk_s10_weather_logged, 1.25),
]
