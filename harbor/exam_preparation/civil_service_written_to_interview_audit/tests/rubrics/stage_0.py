from __future__ import annotations

from ._helpers import check_by_id

def stage_00_dashboard_created(env) -> bool:
    return check_by_id(env, 'stage_00_dashboard_created')

def stage_00_auth_boundary_logged(env) -> bool:
    return check_by_id(env, 'stage_00_auth_boundary_logged')

CHECKS = [
    ('stage_00_dashboard_created', stage_00_dashboard_created, 1.0),
    ('stage_00_auth_boundary_logged', stage_00_auth_boundary_logged, 1.5),
]
