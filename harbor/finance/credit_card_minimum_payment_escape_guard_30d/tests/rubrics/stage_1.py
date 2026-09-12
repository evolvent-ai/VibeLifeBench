"""Stage 1 business-state checks."""
from __future__ import annotations
from .stage_checks import check_stage_business,check_stage_evidence,check_stage_boundary

def s1_business(env): return check_stage_business(env,1)
def s1_evidence(env): return check_stage_evidence(env,1)
CHECKS=[('s1_business',s1_business,2.0),('s1_evidence',s1_evidence,4.0)]
