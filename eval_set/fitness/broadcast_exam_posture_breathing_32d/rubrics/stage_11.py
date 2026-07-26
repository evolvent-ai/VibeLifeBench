from __future__ import annotations
from ._helpers import evaluate

def chk_s11_weather_preemptive(env) -> bool:
    return evaluate('chk_s11_weather_preemptive', env)

CHECKS = [
    ('chk_s11_weather_preemptive', chk_s11_weather_preemptive, 1.25),
]
