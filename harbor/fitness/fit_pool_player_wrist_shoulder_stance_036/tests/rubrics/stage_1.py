from __future__ import annotations
from ._helpers import _check

def chk_s01_health_baseline_recorded(env) -> bool:
    return _check('chk_s01_health_baseline_recorded', env)

def chk_s01_pain_threshold_set(env) -> bool:
    return _check('chk_s01_pain_threshold_set', env)

CHECKS = [
    ('chk_s01_health_baseline_recorded', chk_s01_health_baseline_recorded, 1.25),
    ('chk_s01_pain_threshold_set', chk_s01_pain_threshold_set, 1.5),
]
