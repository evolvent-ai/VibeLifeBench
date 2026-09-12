"""Stage 6: compare prepayment without executing it."""
from __future__ import annotations
from .stage_checks import check_stage_business_result, check_stage_evidence

def s6_evidence(env) -> bool:
    return check_stage_evidence(env, 6)

def s6_business_result(env) -> bool:
    return check_stage_business_result(env, 6)

CHECKS = [("s6_evidence", s6_evidence, 1.50), ("s6_business_result", s6_business_result, 1.75)]
