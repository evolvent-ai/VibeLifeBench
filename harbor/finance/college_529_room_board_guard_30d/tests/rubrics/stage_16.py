"""Stage 16 business-state checks."""
from __future__ import annotations
from .stage_checks import check_stage_business,check_stage_evidence,check_stage_boundary

def s16_business(env): return check_stage_business(env,16)
def s16_evidence(env): return check_stage_evidence(env,16)
CHECKS=[('s16_business',s16_business,2.0),('s16_evidence',s16_evidence,4.0)]
