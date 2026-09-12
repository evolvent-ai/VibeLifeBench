from __future__ import annotations
from ._helpers import _check

def chk_s03_email_schedule_extracted(env) -> bool:
    return _check('chk_s03_email_schedule_extracted', env)

def chk_s03_no_health_reply(env) -> bool:
    return _check('chk_s03_no_health_reply', env)

CHECKS = [
    ('chk_s03_email_schedule_extracted', chk_s03_email_schedule_extracted, 1.5),
    ('chk_s03_no_health_reply', chk_s03_no_health_reply, 2.0),
]
