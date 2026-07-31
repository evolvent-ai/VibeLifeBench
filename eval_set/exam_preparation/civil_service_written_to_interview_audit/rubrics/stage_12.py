from __future__ import annotations

from ._helpers import check_by_id

def stage_12_scheduled_ticket_recheck(env) -> bool:
    return check_by_id(env, 'stage_12_scheduled_ticket_recheck')

CHECKS = [
    ('stage_12_scheduled_ticket_recheck', stage_12_scheduled_ticket_recheck, 1.5),
]
