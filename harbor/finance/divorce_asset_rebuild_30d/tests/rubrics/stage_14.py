"""Stage 14: both payment objects and new balances reconciled."""
from __future__ import annotations
from .stage_checks import check_stage_business_result, check_stage_evidence

def s14_evidence(env) -> bool:
    return check_stage_evidence(env, 14)

def s14_business_result(env) -> bool:
    return check_stage_business_result(env, 14)

CHECKS = [("s14_evidence", s14_evidence, 1.50), ("s14_business_result", s14_business_result, 1.75)]
