from __future__ import annotations
from ._helpers import check_s7_shanghai_window_plan

def s7_shanghai_window_plan(env) -> bool:
    return check_s7_shanghai_window_plan(env)

CHECKS = [
    ("s7_shanghai_window_plan", s7_shanghai_window_plan, 3),
]
