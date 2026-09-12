"""Stage 6 business-state checks."""
from __future__ import annotations
from .stage_checks import check_stage_business,check_stage_evidence,check_stage_boundary

def s6_business(env): return check_stage_business(env,6)
def s6_evidence(env): return check_stage_evidence(env,6)
CHECKS=[('s6_business',s6_business,2.0),('s6_evidence',s6_evidence,4.0)]
