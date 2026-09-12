"""Stage 12 business-state checks."""
from __future__ import annotations
from .stage_checks import check_stage_business,check_stage_evidence,check_stage_boundary

def s12_business(env): return check_stage_business(env,12)
def s12_evidence(env): return check_stage_evidence(env,12)
def s12_boundary(env): return check_stage_boundary(env,12)

CHECKS=[('s12_business',s12_business,2.0),('s12_evidence',s12_evidence,4.0),('s12_boundary',s12_boundary,4.0)]
