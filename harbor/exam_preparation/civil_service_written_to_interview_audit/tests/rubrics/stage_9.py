from __future__ import annotations

from ._helpers import check_by_id

def stage_09_course_compared(env) -> bool:
    return check_by_id(env, 'stage_09_course_compared')

CHECKS = [
    ('stage_09_course_compared', stage_09_course_compared, 1.75),
]
