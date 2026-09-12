from __future__ import annotations
from ._helpers import _check

def chk_s15_sleep_shoulder_risk_detected(env) -> bool:
    return _check('chk_s15_sleep_shoulder_risk_detected', env)

def chk_s15_recovery_calendar_updated(env) -> bool:
    return _check('chk_s15_recovery_calendar_updated', env)

CHECKS = [
    ('chk_s15_sleep_shoulder_risk_detected', chk_s15_sleep_shoulder_risk_detected, 1.5),
    ('chk_s15_recovery_calendar_updated', chk_s15_recovery_calendar_updated, 2.0),
]
