from __future__ import annotations
from ._helpers import evaluate

def chk_s13_weather_mutation_discovered(env) -> bool:
    return evaluate('chk_s13_weather_mutation_discovered', env)

def chk_s13_voice_cold_protection(env) -> bool:
    return evaluate('chk_s13_voice_cold_protection', env)

CHECKS = [
    ('chk_s13_weather_mutation_discovered', chk_s13_weather_mutation_discovered, 2.0),
    ('chk_s13_voice_cold_protection', chk_s13_voice_cold_protection, 1.5),
]
