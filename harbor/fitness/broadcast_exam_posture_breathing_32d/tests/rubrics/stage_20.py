from __future__ import annotations
from ._helpers import evaluate

def chk_s20_rehearsal_mail_calendar_link(env) -> bool:
    return evaluate('chk_s20_rehearsal_mail_calendar_link', env)

def chk_s20_taper_start(env) -> bool:
    return evaluate('chk_s20_taper_start', env)

CHECKS = [
    ('chk_s20_rehearsal_mail_calendar_link', chk_s20_rehearsal_mail_calendar_link, 1.75),
    ('chk_s20_taper_start', chk_s20_taper_start, 2.0),
]
