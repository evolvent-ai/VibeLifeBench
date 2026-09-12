from __future__ import annotations
from ._helpers import *

def s14_detect_office_b_change(env) -> bool:
    return run_stage_requirement(env, 's14_detect_office_b_change')

def s14_mark_a_snapshot_stale(env) -> bool:
    return run_stage_requirement(env, 's14_mark_a_snapshot_stale')

CHECKS = [
    ('s14_detect_office_b_change', s14_detect_office_b_change, 1.75),
    ('s14_mark_a_snapshot_stale', s14_mark_a_snapshot_stale, 1.25),
]
