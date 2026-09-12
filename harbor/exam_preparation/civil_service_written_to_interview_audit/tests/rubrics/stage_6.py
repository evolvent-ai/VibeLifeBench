from __future__ import annotations

from ._helpers import check_by_id

def stage_06_thesis_conflict_adjusted(env) -> bool:
    return check_by_id(env, 'stage_06_thesis_conflict_adjusted')

CHECKS = [
    ('stage_06_thesis_conflict_adjusted', stage_06_thesis_conflict_adjusted, 1.5),
]
