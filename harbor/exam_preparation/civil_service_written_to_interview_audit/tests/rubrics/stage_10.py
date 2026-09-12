from __future__ import annotations

from ._helpers import check_by_id

def stage_10_review_mutation_recorded(env) -> bool:
    return check_by_id(env, 'stage_10_review_mutation_recorded')

CHECKS = [
    ('stage_10_review_mutation_recorded', stage_10_review_mutation_recorded, 1.5),
]
