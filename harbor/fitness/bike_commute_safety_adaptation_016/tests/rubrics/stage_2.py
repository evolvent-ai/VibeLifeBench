from __future__ import annotations
from ._helpers import _check

def chk_s02_calendar_weather_recovery_plan(env) -> bool:
    return _check('chk_s02_calendar_weather_recovery_plan', env)

CHECKS = [
    ('chk_s02_calendar_weather_recovery_plan', chk_s02_calendar_weather_recovery_plan, 1.5),
]
