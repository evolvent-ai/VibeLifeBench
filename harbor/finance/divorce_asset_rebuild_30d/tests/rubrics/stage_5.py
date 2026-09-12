"""Stage 5: mortgage quote, contract rate, and joint liability."""
from __future__ import annotations
from .stage_checks import check_stage_business_result, check_stage_evidence

def s5_evidence(env) -> bool:
    return check_stage_evidence(env, 5)

def s5_business_result(env) -> bool:
    return check_stage_business_result(env, 5)

CHECKS = [("s5_evidence", s5_evidence, 1.50), ("s5_business_result", s5_business_result, 1.75)]
