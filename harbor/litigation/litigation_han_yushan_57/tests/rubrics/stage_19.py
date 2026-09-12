from __future__ import annotations
from ._helpers import semantic_check

def s19_candidate_followup_refreshed(env) -> bool:
    return semantic_check(env, 's19_candidate_followup_refreshed')

CHECKS = [
    ('s19_candidate_followup_refreshed', s19_candidate_followup_refreshed, 1.5),
]
