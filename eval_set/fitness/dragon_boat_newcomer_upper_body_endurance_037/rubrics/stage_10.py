from __future__ import annotations
from ._helpers import _check

def chk_s10_weather_thunderstorm_mutation(env) -> bool:
    return _check('chk_s10_weather_thunderstorm_mutation', env)

def chk_s10_thunderstorm_alternative(env) -> bool:
    return _check('chk_s10_thunderstorm_alternative', env)

def chk_s10_weather_calendar_action_light(env) -> bool:
    return _check('chk_s10_weather_calendar_action_light', env)

CHECKS = [
    ('chk_s10_weather_thunderstorm_mutation', chk_s10_weather_thunderstorm_mutation, 1.75),
    ('chk_s10_thunderstorm_alternative', chk_s10_thunderstorm_alternative, 2.0),
    ('chk_s10_weather_calendar_action_light', chk_s10_weather_calendar_action_light, 1.0)
]
