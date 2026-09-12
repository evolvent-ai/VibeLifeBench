from __future__ import annotations

from ._helpers import rule_ok

def s01_registration_email_captured(env) -> bool:
    return rule_ok(env, 's01_registration_email_captured')

def s01_registration_trace_anchor(env) -> bool:
    return rule_ok(env, 's01_registration_trace_anchor')

def s01_calendar_oral_exam_hold(env) -> bool:
    return rule_ok(env, 's01_calendar_oral_exam_hold')

CHECKS = [
    ('s01_registration_email_captured', s01_registration_email_captured, 1.5),
    ('s01_registration_trace_anchor', s01_registration_trace_anchor, 1.0),
    ('s01_calendar_oral_exam_hold', s01_calendar_oral_exam_hold, 1.25),
]
