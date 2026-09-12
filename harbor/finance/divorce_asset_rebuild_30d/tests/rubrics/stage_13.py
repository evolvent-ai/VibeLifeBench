"""Stage 13: exactly two authorized card payments."""
from __future__ import annotations
from .stage_checks import check_stage_business_result, check_stage_evidence

def s13_evidence(env) -> bool:
    return check_stage_evidence(env, 13)

def s13_business_result(env) -> bool:
    return check_stage_business_result(env, 13)

CHECKS = [("s13_evidence", s13_evidence, 1.50), ("s13_business_result", s13_business_result, 1.75)]
