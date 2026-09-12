from __future__ import annotations
from ._helpers import _check

def chk_s17_rain_no_outdoor_ride(env) -> bool:
    return _check('chk_s17_rain_no_outdoor_ride', env)

def chk_s17_weather_order_integrated(env) -> bool:
    return _check('chk_s17_weather_order_integrated', env)

CHECKS = [
    ('chk_s17_rain_no_outdoor_ride', chk_s17_rain_no_outdoor_ride, 2.0),
    ('chk_s17_weather_order_integrated', chk_s17_weather_order_integrated, 1.5),
]
