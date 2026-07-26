from __future__ import annotations
from ._helpers import _check

def chk_s26_race_week_taper_safety(env) -> bool:
    return _check('chk_s26_race_week_taper_safety', env)

def chk_s26_late_weather_health_refresh_light(env) -> bool:
    return _check('chk_s26_late_weather_health_refresh_light', env)

CHECKS = [
    ('chk_s26_race_week_taper_safety', chk_s26_race_week_taper_safety, 2.0),
    ('chk_s26_late_weather_health_refresh_light', chk_s26_late_weather_health_refresh_light, 1.0)
]
