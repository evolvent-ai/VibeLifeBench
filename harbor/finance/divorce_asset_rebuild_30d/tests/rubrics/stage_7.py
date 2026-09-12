"""Stage 7: insurance renewal and relationship-change status."""
from __future__ import annotations
from .stage_checks import check_stage_business_result, check_stage_evidence

def s7_evidence(env) -> bool:
    return check_stage_evidence(env, 7)

def s7_business_result(env) -> bool:
    return check_stage_business_result(env, 7)

CHECKS = [("s7_evidence", s7_evidence, 1.50), ("s7_business_result", s7_business_result, 1.75)]
