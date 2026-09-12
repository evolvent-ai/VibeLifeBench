from __future__ import annotations
from ._helpers import semantic_check

def s4_gap_review_calendar_created(env) -> bool:
    return semantic_check(env, 's4_gap_review_calendar_created')

def s4_evidence_gap_list_updated(env) -> bool:
    return semantic_check(env, 's4_evidence_gap_list_updated')

CHECKS = [
    ('s4_gap_review_calendar_created', s4_gap_review_calendar_created, 1.5),
    ('s4_evidence_gap_list_updated', s4_evidence_gap_list_updated, 1.75),
]
