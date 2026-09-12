"""Stage 0: discover live accounts and services before planning."""
from __future__ import annotations
from .stage_checks import check_stage_business_result, check_stage_evidence

def s0_evidence(env) -> bool:
    return check_stage_evidence(env, 0)

def s0_business_result(env) -> bool:
    return check_stage_business_result(env, 0)

CHECKS = [("s0_evidence", s0_evidence, 1.50), ("s0_business_result", s0_business_result, 1.75)]
