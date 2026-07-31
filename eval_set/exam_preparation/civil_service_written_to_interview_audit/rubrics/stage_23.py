from __future__ import annotations

from ._helpers import check_by_id

def stage_23_xuexin_validity_updated(env) -> bool:
    return check_by_id(env, 'stage_23_xuexin_validity_updated')

CHECKS = [
    ('stage_23_xuexin_validity_updated', stage_23_xuexin_validity_updated, 1.75),
]
