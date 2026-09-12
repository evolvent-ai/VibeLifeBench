from __future__ import annotations

from ._helpers import check_by_id

def stage_07_supplement_recovered(env) -> bool:
    return check_by_id(env, 'stage_07_supplement_recovered')

def stage_07_nl14380_risk_marked(env) -> bool:
    return check_by_id(env, 'stage_07_nl14380_risk_marked')

CHECKS = [
    ('stage_07_supplement_recovered', stage_07_supplement_recovered, 1.75),
    ('stage_07_nl14380_risk_marked', stage_07_nl14380_risk_marked, 1.75),
]
