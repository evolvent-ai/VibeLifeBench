from __future__ import annotations
from ._helpers import _check

def chk_s19_family_conflict_rescheduled(env) -> bool:
    return _check('chk_s19_family_conflict_rescheduled', env)

CHECKS = [
    ('chk_s19_family_conflict_rescheduled', chk_s19_family_conflict_rescheduled, 1.5)
]
