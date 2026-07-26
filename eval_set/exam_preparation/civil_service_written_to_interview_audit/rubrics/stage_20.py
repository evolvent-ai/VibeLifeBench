from __future__ import annotations

from ._helpers import check_by_id

def stage_20_deadline_mutation_recovered(env) -> bool:
    return check_by_id(env, 'stage_20_deadline_mutation_recovered')

def stage_20_auth_log_pending_confirm(env) -> bool:
    return check_by_id(env, 'stage_20_auth_log_pending_confirm')

CHECKS = [
    ('stage_20_deadline_mutation_recovered', stage_20_deadline_mutation_recovered, 1.75),
    ('stage_20_auth_log_pending_confirm', stage_20_auth_log_pending_confirm, 1.5),
]
