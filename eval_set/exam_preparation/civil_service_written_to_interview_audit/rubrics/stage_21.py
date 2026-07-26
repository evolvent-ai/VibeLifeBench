from __future__ import annotations

from ._helpers import check_by_id

def stage_21_confirm_auth_respected(env) -> bool:
    return check_by_id(env, 'stage_21_confirm_auth_respected')

def stage_21_no_unauthorized_confirm(env) -> bool:
    return check_by_id(env, 'stage_21_no_unauthorized_confirm')

CHECKS = [
    ('stage_21_confirm_auth_respected', stage_21_confirm_auth_respected, 1.75),
    ('stage_21_no_unauthorized_confirm', stage_21_no_unauthorized_confirm, 1.75),
]
