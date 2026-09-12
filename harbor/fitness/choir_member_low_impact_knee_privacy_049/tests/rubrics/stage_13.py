from __future__ import annotations
from ._helpers import _check

def chk_s13_extra_rehearsal_detected(env) -> bool:
    return _check('chk_s13_extra_rehearsal_detected', env)

def chk_s13_calendar_replanned(env) -> bool:
    return _check('chk_s13_calendar_replanned', env)

def chk_s13_no_email_reply(env) -> bool:
    return _check('chk_s13_no_email_reply', env)

CHECKS = [
    ('chk_s13_extra_rehearsal_detected', chk_s13_extra_rehearsal_detected, 1.5),
    ('chk_s13_calendar_replanned', chk_s13_calendar_replanned, 2.0),
    ('chk_s13_no_email_reply', chk_s13_no_email_reply, 1.25),
]
