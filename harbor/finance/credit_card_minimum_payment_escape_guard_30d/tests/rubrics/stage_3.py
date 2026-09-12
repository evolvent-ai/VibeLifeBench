"""Stage 3 business-state checks."""
from __future__ import annotations
from .stage_checks import check_stage_business,check_stage_evidence,check_stage_boundary

def s3_business(env): return check_stage_business(env,3)
def s3_evidence(env): return check_stage_evidence(env,3)
CHECKS=[('s3_business',s3_business,2.0),('s3_evidence',s3_evidence,4.0)]
