from __future__ import annotations
from ._helpers import stage_primary, stage_verified_update, stage_boundary

SAFETY_STAGES={4,12,15,20,22,23}

def check_stage_business(env,stage): return stage_primary(env,stage)
def check_stage_evidence(env,stage): return stage_verified_update(env,stage)
def check_stage_boundary(env,stage): return stage_boundary(env,stage)
