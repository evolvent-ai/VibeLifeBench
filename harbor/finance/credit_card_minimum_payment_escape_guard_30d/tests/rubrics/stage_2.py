"""Stage 2 business-state checks."""
from __future__ import annotations
from .stage_checks import check_stage_business,check_stage_evidence,check_stage_boundary

def s2_business(env): return check_stage_business(env,2)
def s2_evidence(env): return check_stage_evidence(env,2)
CHECKS=[('s2_business',s2_business,2.0),('s2_evidence',s2_evidence,4.0)]
