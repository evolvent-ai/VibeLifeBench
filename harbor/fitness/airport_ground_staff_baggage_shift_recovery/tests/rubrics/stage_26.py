from __future__ import annotations
from ._helpers import evaluate

def chk_calendar_final_prep(env) -> bool:
    return evaluate('chk_calendar_final_prep', env)

def chk_crosswind_rain_alt(env) -> bool:
    return evaluate('chk_crosswind_rain_alt', env)

CHECKS = [
    ('chk_calendar_final_prep', chk_calendar_final_prep, 2.0),
    ('chk_crosswind_rain_alt', chk_crosswind_rain_alt, 2.0),
]
