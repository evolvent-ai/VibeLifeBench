from __future__ import annotations
from ._helpers import _check

def chk_s02_release_window(env) -> bool:
    return _check('chk_s02_release_window', env)

def chk_s02_diff_release_email_calendar_lite(env) -> bool:
    return _check('chk_s02_diff_release_email_calendar_lite', env)

CHECKS = [
    ('chk_s02_release_window', chk_s02_release_window, 1.5),
    ('chk_s02_diff_release_email_calendar_lite', chk_s02_diff_release_email_calendar_lite, 1.0),
]
