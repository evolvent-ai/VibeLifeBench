from __future__ import annotations
from ._helpers import evaluate

def chk_s24_pre_exam_no_new_load(env) -> bool:
    return evaluate('chk_s24_pre_exam_no_new_load', env)

def chk_s24_final_checklist(env) -> bool:
    return evaluate('chk_s24_final_checklist', env)

CHECKS = [
    ('chk_s24_pre_exam_no_new_load', chk_s24_pre_exam_no_new_load, 2.0),
    ('chk_s24_final_checklist', chk_s24_final_checklist, 1.25),
]
