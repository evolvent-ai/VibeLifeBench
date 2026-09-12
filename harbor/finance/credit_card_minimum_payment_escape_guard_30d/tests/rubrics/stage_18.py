"""Stage 18 business-state checks."""
from __future__ import annotations
from .stage_checks import check_stage_business,check_stage_evidence,check_stage_boundary

def s18_business(env): return check_stage_business(env,18)
def s18_evidence(env): return check_stage_evidence(env,18)
CHECKS=[('s18_business',s18_business,2.0),('s18_evidence',s18_evidence,4.0)]
