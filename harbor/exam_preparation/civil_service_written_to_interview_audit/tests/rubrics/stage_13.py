from __future__ import annotations

from ._helpers import check_by_id

def stage_13_gate_change_recovered(env) -> bool:
    return check_by_id(env, 'stage_13_gate_change_recovered')

def stage_13_route_calendar_updated(env) -> bool:
    return check_by_id(env, 'stage_13_route_calendar_updated')

CHECKS = [
    ('stage_13_gate_change_recovered', stage_13_gate_change_recovered, 1.75),
    ('stage_13_route_calendar_updated', stage_13_route_calendar_updated, 1.5),
]
