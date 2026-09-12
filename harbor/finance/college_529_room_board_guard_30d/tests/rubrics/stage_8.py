"""Stage 8 business-state checks."""
from __future__ import annotations
from .stage_checks import check_stage_business,check_stage_evidence,check_stage_boundary

def s8_business(env): return check_stage_business(env,8)
def s8_evidence(env): return check_stage_evidence(env,8)
CHECKS=[('s8_business',s8_business,2.0),('s8_evidence',s8_evidence,4.0)]
