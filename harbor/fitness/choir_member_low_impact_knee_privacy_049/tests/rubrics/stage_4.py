from __future__ import annotations
from ._helpers import _check

def chk_s04_weather_baseline_logged(env) -> bool:
    return _check('chk_s04_weather_baseline_logged', env)

def chk_s04_avoid_midday_heat(env) -> bool:
    return _check('chk_s04_avoid_midday_heat', env)

CHECKS = [
    ('chk_s04_weather_baseline_logged', chk_s04_weather_baseline_logged, 1.25),
    ('chk_s04_avoid_midday_heat', chk_s04_avoid_midday_heat, 1.25),
]
