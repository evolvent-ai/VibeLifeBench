from __future__ import annotations

from ._helpers import check_by_id

def stage_05_uncertain_boundary_reply(env) -> bool:
    return check_by_id(env, 'stage_05_uncertain_boundary_reply')

def stage_05_consult_draft_prepared(env) -> bool:
    return check_by_id(env, 'stage_05_consult_draft_prepared')

CHECKS = [
    ('stage_05_uncertain_boundary_reply', stage_05_uncertain_boundary_reply, 1.5),
    ('stage_05_consult_draft_prepared', stage_05_consult_draft_prepared, 1.5),
]
