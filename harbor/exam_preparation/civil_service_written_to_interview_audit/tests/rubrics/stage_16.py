from __future__ import annotations

from ._helpers import check_by_id

def stage_16_score_calendar_created(env) -> bool:
    return check_by_id(env, 'stage_16_score_calendar_created')

CHECKS = [
    ('stage_16_score_calendar_created', stage_16_score_calendar_created, 1.5),
]
