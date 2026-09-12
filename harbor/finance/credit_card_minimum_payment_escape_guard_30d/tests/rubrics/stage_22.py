"""Stage 22 business-state checks."""
from __future__ import annotations
from .stage_checks import check_stage_business,check_stage_evidence,check_stage_boundary

def s22_business(env): return check_stage_business(env,22)
def s22_evidence(env): return check_stage_evidence(env,22)
def s22_boundary(env): return check_stage_boundary(env,22)

CHECKS=[('s22_business',s22_business,2.0),('s22_evidence',s22_evidence,4.0),('s22_boundary',s22_boundary,4.0)]
