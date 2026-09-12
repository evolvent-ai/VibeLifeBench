from __future__ import annotations
from ._helpers import _check

def chk_s01_baseline_calendar_health(env) -> bool:
    return _check('chk_s01_baseline_calendar_health', env)

def chk_cb_s01_baseline_started(env) -> bool:
    return _check('chk_cb_s01_baseline_started', env)

CHECKS = [
    ('chk_s01_baseline_calendar_health', chk_s01_baseline_calendar_health, 1.5),
    ('chk_cb_s01_baseline_started', chk_cb_s01_baseline_started, 1.0),
]
