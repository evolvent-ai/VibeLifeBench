"""Stage 10 business-state checks."""
from __future__ import annotations
from .stage_checks import check_stage_business,check_stage_evidence,check_stage_boundary

def s10_business(env): return check_stage_business(env,10)
def s10_evidence(env): return check_stage_evidence(env,10)
CHECKS=[('s10_business',s10_business,2.0),('s10_evidence',s10_evidence,4.0)]
