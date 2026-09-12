"""Stage 8: policy amounts, dates, and incomplete relationship change."""
from __future__ import annotations
from .stage_checks import check_stage_business_result, check_stage_evidence

def s8_evidence(env) -> bool:
    return check_stage_evidence(env, 8)

def s8_business_result(env) -> bool:
    return check_stage_business_result(env, 8)

CHECKS = [("s8_evidence", s8_evidence, 1.50), ("s8_business_result", s8_business_result, 1.75)]
