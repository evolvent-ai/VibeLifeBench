from __future__ import annotations
from ._helpers import *

def s5_read_short_replies(env) -> bool:
    return run_stage_requirement(env, 's5_read_short_replies')

def s5_triage_discount_noise(env) -> bool:
    return run_stage_requirement(env, 's5_triage_discount_noise')

CHECKS = [
    ('s5_read_short_replies', s5_read_short_replies, 1.25),
    ('s5_triage_discount_noise', s5_triage_discount_noise, 1.0),
]
