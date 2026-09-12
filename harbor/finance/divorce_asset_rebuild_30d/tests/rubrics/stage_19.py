"""Stage 19: three mortgage choices compared against liquidity needs."""
from __future__ import annotations
from .stage_checks import check_stage_business_result, check_stage_evidence

def s19_evidence(env) -> bool:
    return check_stage_evidence(env, 19)

def s19_business_result(env) -> bool:
    return check_stage_business_result(env, 19)

CHECKS = [("s19_evidence", s19_evidence, 1.50), ("s19_business_result", s19_business_result, 1.75)]
