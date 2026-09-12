from __future__ import annotations
from ._helpers import semantic_check

def s11_candidate_expiry_rechecked(env) -> bool:
    return semantic_check(env, 's11_candidate_expiry_rechecked')

def s11_candidate_risk_versioned(env) -> bool:
    return semantic_check(env, 's11_candidate_risk_versioned')

CHECKS = [
    ('s11_candidate_expiry_rechecked', s11_candidate_expiry_rechecked, 1.75),
    ('s11_candidate_risk_versioned', s11_candidate_risk_versioned, 1.5),
]
