from __future__ import annotations
from . import _helpers as H

def s17_course_cancel_recovered(env) -> bool:
    return H.s17_course_cancel_recovered(env)

def s17_course_cancel_light_refresh(env) -> bool:
    return H.s17_course_cancel_light_refresh(env)

def s17_no_cancelled_course_order(env) -> bool:
    return H.s17_no_cancelled_course_order(env)

CHECKS = [
    ("s17_course_cancel_recovered", s17_course_cancel_recovered, 1.75),
    ("s17_course_cancel_light_refresh", s17_course_cancel_light_refresh, 1.0),
    ("s17_no_cancelled_course_order", s17_no_cancelled_course_order, 1.75)
]
