from __future__ import annotations

from ._helpers import check_by_id

def stage_01_post_source_recorded(env) -> bool:
    return check_by_id(env, 'stage_01_post_source_recorded')

def stage_01_matrix_initialized(env) -> bool:
    return check_by_id(env, 'stage_01_matrix_initialized')

CHECKS = [
    ('stage_01_post_source_recorded', stage_01_post_source_recorded, 1.5),
    ('stage_01_matrix_initialized', stage_01_matrix_initialized, 1.75),
]
