from __future__ import annotations
from ._helpers import semantic_check

def s15_mediation_window_updated(env) -> bool:
    return semantic_check(env, 's15_mediation_window_updated')

def s15_no_mediation_submission(env) -> bool:
    return semantic_check(env, 's15_no_mediation_submission')

CHECKS = [
    ('s15_mediation_window_updated', s15_mediation_window_updated, 1.5),
    ('s15_no_mediation_submission', s15_no_mediation_submission, 2.0),
]
