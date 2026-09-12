from __future__ import annotations
from ._helpers import _check

def chk_s01_baseline_health_calendar(env) -> bool:
    return _check('chk_s01_baseline_health_calendar', env)

CHECKS = [
    ('chk_s01_baseline_health_calendar', chk_s01_baseline_health_calendar, 1.5)
]
