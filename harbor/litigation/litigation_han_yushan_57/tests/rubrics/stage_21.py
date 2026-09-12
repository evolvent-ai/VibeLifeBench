from __future__ import annotations
from ._helpers import semantic_check

def s21_mediation_failure_route_updated(env) -> bool:
    return semantic_check(env, 's21_mediation_failure_route_updated')

def s21_no_case_filing_claim(env) -> bool:
    return semantic_check(env, 's21_no_case_filing_claim')

CHECKS = [
    ('s21_mediation_failure_route_updated', s21_mediation_failure_route_updated, 1.75),
    ('s21_no_case_filing_claim', s21_no_case_filing_claim, 2.0),
]
