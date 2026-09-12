"""Stage 17 business-state checks."""
from __future__ import annotations
from .stage_checks import check_stage_business,check_stage_evidence,check_stage_boundary

def s17_business(env): return check_stage_business(env,17)
def s17_evidence(env): return check_stage_evidence(env,17)
CHECKS=[('s17_business',s17_business,2.0),('s17_evidence',s17_evidence,4.0)]
