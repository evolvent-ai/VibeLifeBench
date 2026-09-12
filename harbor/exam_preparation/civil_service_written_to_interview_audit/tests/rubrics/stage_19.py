from __future__ import annotations

from ._helpers import check_by_id

def stage_19_score_line_processed(env) -> bool:
    return check_by_id(env, 'stage_19_score_line_processed')

def stage_19_nl14308_interview_priority(env) -> bool:
    return check_by_id(env, 'stage_19_nl14308_interview_priority')

CHECKS = [
    ('stage_19_score_line_processed', stage_19_score_line_processed, 1.75),
    ('stage_19_nl14308_interview_priority', stage_19_nl14308_interview_priority, 1.75),
]
