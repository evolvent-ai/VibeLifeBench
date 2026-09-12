"""Stage 14 business-state checks."""
from __future__ import annotations
from .stage_checks import check_stage_business,check_stage_evidence,check_stage_boundary

def s14_business(env): return check_stage_business(env,14)
def s14_evidence(env): return check_stage_evidence(env,14)
CHECKS=[('s14_business',s14_business,2.0),('s14_evidence',s14_evidence,4.0)]
