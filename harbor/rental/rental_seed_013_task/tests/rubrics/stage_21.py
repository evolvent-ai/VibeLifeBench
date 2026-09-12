from __future__ import annotations
from ._helpers import *

def s21_detect_long202_price_drop(env) -> bool:
    return run_stage_requirement(env, 's21_detect_long202_price_drop')

def s21_request_viewing_window_confirmation(env) -> bool:
    return run_stage_requirement(env, 's21_request_viewing_window_confirmation')

CHECKS = [
    ('s21_detect_long202_price_drop', s21_detect_long202_price_drop, 1.75),
    ('s21_request_viewing_window_confirmation', s21_request_viewing_window_confirmation, 1.25),
]
