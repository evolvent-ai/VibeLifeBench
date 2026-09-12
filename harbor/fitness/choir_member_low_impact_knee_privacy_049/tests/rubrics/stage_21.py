from __future__ import annotations
from ._helpers import _check

def chk_s21_calltime_extracted(env) -> bool:
    return _check('chk_s21_calltime_extracted', env)

def chk_s21_taper_window_created(env) -> bool:
    return _check('chk_s21_taper_window_created', env)

def chk_s21_no_email_sent(env) -> bool:
    return _check('chk_s21_no_email_sent', env)

CHECKS = [
    ('chk_s21_calltime_extracted', chk_s21_calltime_extracted, 1.25),
    ('chk_s21_taper_window_created', chk_s21_taper_window_created, 1.5),
    ('chk_s21_no_email_sent', chk_s21_no_email_sent, 1.25),
]
