from __future__ import annotations
from ._helpers import evaluate

def chk_s03_calendar_32d_plan(env) -> bool:
    return evaluate('chk_s03_calendar_32d_plan', env)

def chk_s03_weather_initial_check(env) -> bool:
    return evaluate('chk_s03_weather_initial_check', env)

CHECKS = [
    ('chk_s03_calendar_32d_plan', chk_s03_calendar_32d_plan, 2.0),
    ('chk_s03_weather_initial_check', chk_s03_weather_initial_check, 1.25),
]
