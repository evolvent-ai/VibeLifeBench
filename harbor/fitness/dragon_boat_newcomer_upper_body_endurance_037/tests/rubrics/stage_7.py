from __future__ import annotations
from ._helpers import _check

def chk_s07_work_conflict_reschedule(env) -> bool:
    return _check('chk_s07_work_conflict_reschedule', env)

CHECKS = [
    ('chk_s07_work_conflict_reschedule', chk_s07_work_conflict_reschedule, 1.5)
]
