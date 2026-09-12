from __future__ import annotations
from ._helpers import _check

def chk_s03_first_weather_window(env) -> bool:
    return _check('chk_s03_first_weather_window', env)

CHECKS = [
    ('chk_s03_first_weather_window', chk_s03_first_weather_window, 1.25),
]
