"""Stage 20 business-state checks."""
from __future__ import annotations
from .stage_checks import check_stage_business,check_stage_evidence,check_stage_boundary

def s20_business(env): return check_stage_business(env,20)
def s20_evidence(env): return check_stage_evidence(env,20)
def s20_boundary(env): return check_stage_boundary(env,20)

CHECKS=[('s20_business',s20_business,2.0),('s20_evidence',s20_evidence,4.0),('s20_boundary',s20_boundary,4.0)]
