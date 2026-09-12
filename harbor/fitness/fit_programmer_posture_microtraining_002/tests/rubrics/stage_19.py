from __future__ import annotations
from ._helpers import _check

def chk_s19_work_conflict_split(env) -> bool:
    return _check('chk_s19_work_conflict_split', env)

def chk_s19_diff_conflict_event_replacement_lite(env) -> bool:
    return _check('chk_s19_diff_conflict_event_replacement_lite', env)

CHECKS = [
    ('chk_s19_work_conflict_split', chk_s19_work_conflict_split, 1.5),
    ('chk_s19_diff_conflict_event_replacement_lite', chk_s19_diff_conflict_event_replacement_lite, 1.0),
]
