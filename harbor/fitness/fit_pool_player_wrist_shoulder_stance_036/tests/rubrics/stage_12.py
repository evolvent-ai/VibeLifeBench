from __future__ import annotations
from ._helpers import _check

def chk_s12_wrist_pain_detected(env) -> bool:
    return _check('chk_s12_wrist_pain_detected', env)

def chk_s12_wrist_load_reduced(env) -> bool:
    return _check('chk_s12_wrist_load_reduced', env)

def chk_s12_professional_eval_if_worsens(env) -> bool:
    return _check('chk_s12_professional_eval_if_worsens', env)

CHECKS = [
    ('chk_s12_wrist_pain_detected', chk_s12_wrist_pain_detected, 1.5),
    ('chk_s12_wrist_load_reduced', chk_s12_wrist_load_reduced, 2.0),
    ('chk_s12_professional_eval_if_worsens', chk_s12_professional_eval_if_worsens, 1.25),
]
