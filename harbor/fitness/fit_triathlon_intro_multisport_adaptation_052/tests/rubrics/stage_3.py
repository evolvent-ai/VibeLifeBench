from __future__ import annotations
from ._helpers import _check

def chk_s03_work_conflict_respected(env) -> bool:
    return _check('chk_s03_work_conflict_respected', env)

CHECKS = [
    ('chk_s03_work_conflict_respected', chk_s03_work_conflict_respected, 1.25),
]
