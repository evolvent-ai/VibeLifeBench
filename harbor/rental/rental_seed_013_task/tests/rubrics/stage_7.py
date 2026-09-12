from __future__ import annotations
from ._helpers import *

def s7_detect_short_102_autorenew(env) -> bool:
    return run_stage_requirement(env, 's7_detect_short_102_autorenew')

def s7_condition_short_102_backup(env) -> bool:
    return run_stage_requirement(env, 's7_condition_short_102_backup')

CHECKS = [
    ('s7_detect_short_102_autorenew', s7_detect_short_102_autorenew, 1.75),
    ('s7_condition_short_102_backup', s7_condition_short_102_backup, 1.25),
]
