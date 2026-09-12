from __future__ import annotations
from ._helpers import _check

def chk_s16_weather_health_downgrade(env) -> bool:
    return _check('chk_s16_weather_health_downgrade', env)

CHECKS = [
    ('chk_s16_weather_health_downgrade', chk_s16_weather_health_downgrade, 1.75),
]
