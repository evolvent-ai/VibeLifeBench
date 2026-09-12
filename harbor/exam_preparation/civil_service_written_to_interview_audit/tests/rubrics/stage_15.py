from __future__ import annotations

from ._helpers import check_by_id

def stage_15_exam_done_logged(env) -> bool:
    return check_by_id(env, 'stage_15_exam_done_logged')

CHECKS = [
    ('stage_15_exam_done_logged', stage_15_exam_done_logged, 1.0),
]
