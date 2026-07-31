from __future__ import annotations
from ._helpers import evaluate

def chk_s02_email_exam_read_no_reply(env) -> bool:
    return evaluate('chk_s02_email_exam_read_no_reply', env)

def chk_s02_deadline_calendar_recorded(env) -> bool:
    return evaluate('chk_s02_deadline_calendar_recorded', env)

CHECKS = [
    ('chk_s02_email_exam_read_no_reply', chk_s02_email_exam_read_no_reply, 1.5),
    ('chk_s02_deadline_calendar_recorded', chk_s02_deadline_calendar_recorded, 1.25),
]
