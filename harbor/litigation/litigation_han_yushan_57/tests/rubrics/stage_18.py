from __future__ import annotations
from ._helpers import semantic_check

def s18_second_defense_versioned(env) -> bool:
    return semantic_check(env, 's18_second_defense_versioned')

def s18_appraisal_questions_updated(env) -> bool:
    return semantic_check(env, 's18_appraisal_questions_updated')

CHECKS = [
    ('s18_second_defense_versioned', s18_second_defense_versioned, 1.75),
    ('s18_appraisal_questions_updated', s18_appraisal_questions_updated, 1.5),
]
