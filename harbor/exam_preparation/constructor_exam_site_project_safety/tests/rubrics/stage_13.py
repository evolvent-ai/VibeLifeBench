from ._helpers import (
    response_check_id,
    s13_weather_alert_calendar_unique as _s13_weather_alert_calendar_unique,
    structured_check_id,
)

def s13_weather_alert_refresh(env) -> bool:
    return structured_check_id(env, 's13_weather_alert_refresh')

def s13_weather_alert_calendar_unique(env) -> bool:
    return _s13_weather_alert_calendar_unique(env)

def s13_weather_safety_hold(env) -> bool:
    return response_check_id(env, 's13_weather_safety_hold')

CHECKS = [
    ('s13_weather_alert_refresh', s13_weather_alert_refresh, 1.0),
    ('s13_weather_alert_calendar_unique', s13_weather_alert_calendar_unique, 1.0),
    ('s13_weather_safety_hold', s13_weather_safety_hold, 2.0),
]
