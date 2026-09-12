"""Stage 20: medical policy renewed; other policy work still pending."""
from __future__ import annotations
from .stage_checks import check_stage_business_result, check_stage_evidence

def s20_evidence(env) -> bool:
    return check_stage_evidence(env, 20)

def s20_business_result(env) -> bool:
    return check_stage_business_result(env, 20)

CHECKS = [("s20_evidence", s20_evidence, 1.50), ("s20_business_result", s20_business_result, 1.75)]
