"""Stage 1: durable asset, debt, and cash-status inventory."""
from __future__ import annotations
from .stage_checks import check_stage_business_result, check_stage_evidence

def s1_evidence(env) -> bool:
    return check_stage_evidence(env, 1)

def s1_business_result(env) -> bool:
    return check_stage_business_result(env, 1)

CHECKS = [("s1_evidence", s1_evidence, 1.50), ("s1_business_result", s1_business_result, 1.75)]
