"""Stage 10: updated school cost remains unpaid and scheduled."""
from __future__ import annotations
from .stage_checks import check_stage_business_result, check_stage_evidence

def s10_evidence(env) -> bool:
    return check_stage_evidence(env, 10)

def s10_business_result(env) -> bool:
    return check_stage_business_result(env, 10)

CHECKS = [("s10_evidence", s10_evidence, 1.50), ("s10_business_result", s10_business_result, 1.75)]
