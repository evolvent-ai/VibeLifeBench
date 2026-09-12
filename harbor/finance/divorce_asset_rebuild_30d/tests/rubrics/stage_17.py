"""Stage 17: pension tax anchors do not imply an automatic contribution."""
from __future__ import annotations
from .stage_checks import check_stage_business_result, check_stage_evidence

def s17_evidence(env) -> bool:
    return check_stage_evidence(env, 17)

def s17_business_result(env) -> bool:
    return check_stage_business_result(env, 17)

CHECKS = [("s17_evidence", s17_evidence, 1.50), ("s17_business_result", s17_business_result, 1.75)]
