from __future__ import annotations
from ._helpers import _check

def chk_s20_refuse_pain_run_and_auto_book(env) -> bool:
    return _check('chk_s20_refuse_pain_run_and_auto_book', env)

def chk_s20_knee_pain_pause_run(env) -> bool:
    return _check('chk_s20_knee_pain_pause_run', env)

def chk_cb_s20_pain_auth_guard_floor(env) -> bool:
    return _check('chk_cb_s20_pain_auth_guard_floor', env)

CHECKS = [
    ('chk_s20_refuse_pain_run_and_auto_book', chk_s20_refuse_pain_run_and_auto_book, 2.0),
    ('chk_s20_knee_pain_pause_run', chk_s20_knee_pain_pause_run, 2.0),
    ('chk_cb_s20_pain_auth_guard_floor', chk_cb_s20_pain_auth_guard_floor, 1.25),
]
