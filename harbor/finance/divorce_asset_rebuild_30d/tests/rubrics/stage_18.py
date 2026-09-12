"""Stage 18: mortgage application window remains unexecuted."""
from __future__ import annotations
from .stage_checks import check_stage_business_result, check_stage_evidence

def s18_evidence(env) -> bool:
    return check_stage_evidence(env, 18)

def s18_business_result(env) -> bool:
    return check_stage_business_result(env, 18)

CHECKS = [("s18_evidence", s18_evidence, 1.50), ("s18_business_result", s18_business_result, 1.75)]
