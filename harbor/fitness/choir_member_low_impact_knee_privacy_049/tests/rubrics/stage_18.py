from __future__ import annotations
from ._helpers import _check

def chk_s18_sleep_low_detected(env) -> bool:
    return _check('chk_s18_sleep_low_detected', env)

def chk_s18_training_downgraded(env) -> bool:
    return _check('chk_s18_training_downgraded', env)

def chk_s18_no_compensation_workout(env) -> bool:
    return _check('chk_s18_no_compensation_workout', env)

CHECKS = [
    ('chk_s18_sleep_low_detected', chk_s18_sleep_low_detected, 1.5),
    ('chk_s18_training_downgraded', chk_s18_training_downgraded, 1.75),
    ('chk_s18_no_compensation_workout', chk_s18_no_compensation_workout, 1.25),
]
