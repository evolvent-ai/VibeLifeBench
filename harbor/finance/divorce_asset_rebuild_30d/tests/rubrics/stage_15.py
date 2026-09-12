"""Stage 15: later card interest supersedes the older snapshot."""
from __future__ import annotations
from .stage_checks import check_stage_business_result, check_stage_evidence

def s15_evidence(env) -> bool:
    return check_stage_evidence(env, 15)

def s15_business_result(env) -> bool:
    return check_stage_business_result(env, 15)

CHECKS = [("s15_evidence", s15_evidence, 1.50), ("s15_business_result", s15_business_result, 1.75)]
