from __future__ import annotations
from . import _helpers as H

def s13_travel_load_control(env) -> bool:
    return H.s13_travel_load_control(env)

def s13_di_plan_adjusted(env) -> bool:
    return H.s13_di_plan_adjusted(env)

CHECKS = [
    ("s13_travel_load_control", s13_travel_load_control, 1.25),
    ("s13_di_plan_adjusted", s13_di_plan_adjusted, 1.25)
]
