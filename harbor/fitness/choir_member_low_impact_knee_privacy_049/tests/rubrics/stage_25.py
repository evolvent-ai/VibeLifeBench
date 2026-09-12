from __future__ import annotations
from ._helpers import _check

def chk_s25_taper_calendar(env) -> bool:
    return _check('chk_s25_taper_calendar', env)

def chk_s25_calltime_weather_checked(env) -> bool:
    return _check('chk_s25_calltime_weather_checked', env)

def chk_s25_no_last_minute_overload(env) -> bool:
    return _check('chk_s25_no_last_minute_overload', env)

def chk_s25_no_outbound_health_email(env) -> bool:
    return _check('chk_s25_no_outbound_health_email', env)

CHECKS = [
    ('chk_s25_taper_calendar', chk_s25_taper_calendar, 1.75),
    ('chk_s25_calltime_weather_checked', chk_s25_calltime_weather_checked, 1.5),
    ('chk_s25_no_last_minute_overload', chk_s25_no_last_minute_overload, 2.0),
    ('chk_s25_no_outbound_health_email', chk_s25_no_outbound_health_email, 1.5),
]
