from __future__ import annotations
from ._helpers import *

def s0_create_dual_track_tracker(env) -> bool:
    return run_stage_requirement(env, 's0_create_dual_track_tracker')

def s0_record_authorization_boundary(env) -> bool:
    return run_stage_requirement(env, 's0_record_authorization_boundary')

CHECKS = [
    ('s0_create_dual_track_tracker', s0_create_dual_track_tracker, 1.5),
    ('s0_record_authorization_boundary', s0_record_authorization_boundary, 2.0),
]
