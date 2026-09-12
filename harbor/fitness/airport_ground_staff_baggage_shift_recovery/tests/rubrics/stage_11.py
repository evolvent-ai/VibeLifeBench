from __future__ import annotations
from ._helpers import evaluate

def chk_weather_heat_logged(env) -> bool:
    return evaluate('chk_weather_heat_logged', env)

CHECKS = [
    ('chk_weather_heat_logged', chk_weather_heat_logged, 1.25),
]
