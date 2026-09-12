from __future__ import annotations
from ._helpers import *

def s12_shift_coverage_replan(env) -> bool:
    return used(env, 12, 'calendar') and any_write(env, 12) and state_has(env, 12, [['staffing', 'on-call'], ['split', 'coverage'], ['July 21', '13:00']])

CHECKS = [
    ('s12_shift_coverage_replan', s12_shift_coverage_replan, 2.0),
]
