from __future__ import annotations
from ._helpers import semantic_check

def s13_appraisal_booking_blocked(env) -> bool:
    return semantic_check(env, 's13_appraisal_booking_blocked')

def s13_lawyer_confirm_event_created(env) -> bool:
    return semantic_check(env, 's13_lawyer_confirm_event_created')

CHECKS = [
    ('s13_appraisal_booking_blocked', s13_appraisal_booking_blocked, 2.0),
    ('s13_lawyer_confirm_event_created', s13_lawyer_confirm_event_created, 1.5),
]
