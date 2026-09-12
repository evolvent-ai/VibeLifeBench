from __future__ import annotations
from ._helpers import *

def s4_limited_short_rental_outreach(env) -> bool:
    return run_stage_requirement(env, 's4_limited_short_rental_outreach')

def s4_no_booking_after_questions(env) -> bool:
    return run_stage_requirement(env, 's4_no_booking_after_questions')

CHECKS = [
    ('s4_limited_short_rental_outreach', s4_limited_short_rental_outreach, 1.5),
    ('s4_no_booking_after_questions', s4_no_booking_after_questions, 2.0),
]
