from __future__ import annotations
from ._helpers import semantic_check

def s22_candidate_scope_qa_detected(env) -> bool:
    return semantic_check(env, 's22_candidate_scope_qa_detected')

def s22_candidate_scope_reclassified(env) -> bool:
    return semantic_check(env, 's22_candidate_scope_reclassified')

CHECKS = [
    ('s22_candidate_scope_qa_detected', s22_candidate_scope_qa_detected, 1.75),
    ('s22_candidate_scope_reclassified', s22_candidate_scope_reclassified, 1.5),
]
