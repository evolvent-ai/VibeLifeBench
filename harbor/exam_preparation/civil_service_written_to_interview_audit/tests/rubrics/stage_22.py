from __future__ import annotations

from ._helpers import check_by_id

def stage_22_material_check_completed(env) -> bool:
    return check_by_id(env, 'stage_22_material_check_completed')

CHECKS = [
    ('stage_22_material_check_completed', stage_22_material_check_completed, 1.0),
]
