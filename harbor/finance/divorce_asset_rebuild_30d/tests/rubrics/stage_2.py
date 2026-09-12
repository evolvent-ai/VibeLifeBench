"""Stage 2: delayed support remains a receivable, not cash."""
from __future__ import annotations
from .stage_checks import check_stage_business_result, check_stage_evidence

def s2_evidence(env) -> bool:
    return check_stage_evidence(env, 2)

def s2_business_result(env) -> bool:
    return check_stage_business_result(env, 2)

CHECKS = [("s2_evidence", s2_evidence, 1.50), ("s2_business_result", s2_business_result, 1.75)]
