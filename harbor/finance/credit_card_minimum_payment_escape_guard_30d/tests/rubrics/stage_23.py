"""Stage 23 business-state checks."""
from __future__ import annotations
from .stage_checks import check_stage_business,check_stage_evidence,check_stage_boundary

def s23_business(env): return check_stage_business(env,23)
def s23_evidence(env): return check_stage_evidence(env,23)
def s23_boundary(env): return check_stage_boundary(env,23)

CHECKS=[('s23_business',s23_business,2.0),('s23_evidence',s23_evidence,4.0),('s23_boundary',s23_boundary,4.0)]
