"""Stage 0 business-state checks."""
from __future__ import annotations
from .stage_checks import check_stage_business,check_stage_evidence,check_stage_boundary

def s0_business(env): return check_stage_business(env,0)
def s0_evidence(env): return check_stage_evidence(env,0)
CHECKS=[('s0_business',s0_business,2.0),('s0_evidence',s0_evidence,4.0)]
