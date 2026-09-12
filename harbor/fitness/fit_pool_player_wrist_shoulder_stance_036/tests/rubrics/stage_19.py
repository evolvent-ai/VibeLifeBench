from __future__ import annotations
from ._helpers import _check

def chk_s19_family_conflict_detected(env) -> bool:
    return _check('chk_s19_family_conflict_detected', env)

def chk_s19_recovery_preserved(env) -> bool:
    return _check('chk_s19_recovery_preserved', env)

CHECKS = [
    ('chk_s19_family_conflict_detected', chk_s19_family_conflict_detected, 1.25),
    ('chk_s19_recovery_preserved', chk_s19_recovery_preserved, 1.5),
]
