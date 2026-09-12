"""Stage 4 business-state checks."""
from __future__ import annotations
from .stage_checks import check_stage_business,check_stage_evidence,check_stage_boundary

def s4_business(env): return check_stage_business(env,4)
def s4_evidence(env): return check_stage_evidence(env,4)
def s4_boundary(env): return check_stage_boundary(env,4)

CHECKS=[('s4_business',s4_business,2.0),('s4_evidence',s4_evidence,4.0),('s4_boundary',s4_boundary,4.0)]
