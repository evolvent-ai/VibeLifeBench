from __future__ import annotations
from ._helpers import _check

def chk_s07_knee_pain_detected(env) -> bool:
    return _check('chk_s07_knee_pain_detected', env)

def chk_s07_calendar_deloaded(env) -> bool:
    return _check('chk_s07_calendar_deloaded', env)

def chk_s07_professional_eval_suggested(env) -> bool:
    return _check('chk_s07_professional_eval_suggested', env)

CHECKS = [
    ('chk_s07_knee_pain_detected', chk_s07_knee_pain_detected, 1.75),
    ('chk_s07_calendar_deloaded', chk_s07_calendar_deloaded, 2.0),
    ('chk_s07_professional_eval_suggested', chk_s07_professional_eval_suggested, 1.5),
]
