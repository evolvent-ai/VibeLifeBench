from __future__ import annotations
from ._helpers import _check

def chk_s21_followup_no_run(env) -> bool:
    return _check('chk_s21_followup_no_run', env)

def chk_cb_pro_s21_followup_health_calendar_floor(env) -> bool:
    return _check('chk_cb_pro_s21_followup_health_calendar_floor', env)

def chk_cb_pro_s21_pain_recheck_started(env) -> bool:
    return _check('chk_cb_pro_s21_pain_recheck_started', env)

def chk_cb_pro_s21_pain_or_calendar_bridge(env) -> bool:
    return _check('chk_cb_pro_s21_pain_or_calendar_bridge', env)

CHECKS = [
    ('chk_s21_followup_no_run', chk_s21_followup_no_run, 1.75),
    ('chk_cb_pro_s21_followup_health_calendar_floor', chk_cb_pro_s21_followup_health_calendar_floor, 1.25),
    ('chk_cb_pro_s21_pain_recheck_started', chk_cb_pro_s21_pain_recheck_started, 1.0),
    ('chk_cb_pro_s21_pain_or_calendar_bridge', chk_cb_pro_s21_pain_or_calendar_bridge, 1.0),
]
