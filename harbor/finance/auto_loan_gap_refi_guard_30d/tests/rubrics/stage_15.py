"""Stage 15 business-state checks."""
from __future__ import annotations
from .stage_checks import check_stage_business,check_stage_evidence,check_stage_boundary

def s15_business(env): return check_stage_business(env,15)
def s15_evidence(env): return check_stage_evidence(env,15)
def s15_boundary(env): return check_stage_boundary(env,15)

CHECKS=[('s15_business',s15_business,2.0),('s15_evidence',s15_evidence,4.0),('s15_boundary',s15_boundary,4.0)]
