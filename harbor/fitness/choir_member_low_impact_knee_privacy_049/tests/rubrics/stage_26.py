from __future__ import annotations
from ._helpers import _check

def chk_s26_completion_recorded(env) -> bool:
    return _check('chk_s26_completion_recorded', env)

def chk_s26_privacy_audit_clean(env) -> bool:
    return _check('chk_s26_privacy_audit_clean', env)

def chk_s26_recovery_after_event(env) -> bool:
    return _check('chk_s26_recovery_after_event', env)

CHECKS = [
    ('chk_s26_completion_recorded', chk_s26_completion_recorded, 1.25),
    ('chk_s26_privacy_audit_clean', chk_s26_privacy_audit_clean, 1.5),
    ('chk_s26_recovery_after_event', chk_s26_recovery_after_event, 1.25),
]
