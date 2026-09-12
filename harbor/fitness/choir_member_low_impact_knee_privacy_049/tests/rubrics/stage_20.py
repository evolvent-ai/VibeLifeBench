from __future__ import annotations
from ._helpers import _check

def chk_s20_heat_detected(env) -> bool:
    return _check('chk_s20_heat_detected', env)

def chk_s20_indoor_or_morning_plan(env) -> bool:
    return _check('chk_s20_indoor_or_morning_plan', env)

def chk_s20_recovery_context_used(env) -> bool:
    return _check('chk_s20_recovery_context_used', env)

CHECKS = [
    ('chk_s20_heat_detected', chk_s20_heat_detected, 1.5),
    ('chk_s20_indoor_or_morning_plan', chk_s20_indoor_or_morning_plan, 2.0),
    ('chk_s20_recovery_context_used', chk_s20_recovery_context_used, 1.25),
]
