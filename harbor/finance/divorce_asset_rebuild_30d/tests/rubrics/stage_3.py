"""Stage 3: two-card statement and interest evidence without payment."""
from __future__ import annotations
from .stage_checks import check_stage_business_result, check_stage_evidence

def s3_evidence(env) -> bool:
    return check_stage_evidence(env, 3)

def s3_business_result(env) -> bool:
    return check_stage_business_result(env, 3)

CHECKS = [("s3_evidence", s3_evidence, 1.50), ("s3_business_result", s3_business_result, 1.75)]
