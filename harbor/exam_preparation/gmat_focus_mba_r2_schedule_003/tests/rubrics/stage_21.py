from __future__ import annotations
from . import _helpers as H

def s21_westbridge_code_recovered(env) -> bool:
    return H.s21_westbridge_code_recovered(env)

def s21_official_delay_recovered(env) -> bool:
    return H.s21_official_delay_recovered(env)

CHECKS = [
    ("s21_westbridge_code_recovered", s21_westbridge_code_recovered, 1.75),
    ("s21_official_delay_recovered", s21_official_delay_recovered, 1.75)
]
