from __future__ import annotations
from ._helpers import *

def s18_send_limited_long203_questions(env) -> bool:
    return run_stage_requirement(env, 's18_send_limited_long203_questions')

def s18_schedule_long202_tentative_viewing(env) -> bool:
    return run_stage_requirement(env, 's18_schedule_long202_tentative_viewing')

CHECKS = [
    ('s18_send_limited_long203_questions', s18_send_limited_long203_questions, 1.5),
    ('s18_schedule_long202_tentative_viewing', s18_schedule_long202_tentative_viewing, 1.5),
]
