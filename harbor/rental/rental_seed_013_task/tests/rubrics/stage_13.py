from __future__ import annotations
from ._helpers import *

def s13_send_authorized_hr_question(env) -> bool:
    return run_stage_requirement(env, 's13_send_authorized_hr_question')

def s13_update_short_103_movein_plan(env) -> bool:
    return run_stage_requirement(env, 's13_update_short_103_movein_plan')

CHECKS = [
    ('s13_send_authorized_hr_question', s13_send_authorized_hr_question, 1.75),
    ('s13_update_short_103_movein_plan', s13_update_short_103_movein_plan, 1.5),
]
