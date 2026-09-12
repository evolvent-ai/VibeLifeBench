from __future__ import annotations
from ._helpers import _check

def chk_s02_camp_email_equipment_pending(env) -> bool:
    return _check('chk_s02_camp_email_equipment_pending', env)

def chk_cb_s02_camp_mail_or_calendar_started(env) -> bool:
    return _check('chk_cb_s02_camp_mail_or_calendar_started', env)

CHECKS = [
    ('chk_s02_camp_email_equipment_pending', chk_s02_camp_email_equipment_pending, 1.5),
    ('chk_cb_s02_camp_mail_or_calendar_started', chk_cb_s02_camp_mail_or_calendar_started, 1.0),
]
