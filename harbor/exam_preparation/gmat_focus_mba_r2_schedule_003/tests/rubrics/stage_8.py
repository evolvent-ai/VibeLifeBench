from __future__ import annotations
from . import _helpers as H

def s8_material_budget_shortlist(env) -> bool:
    return H.s8_material_budget_shortlist(env)

def s8_no_course_purchase(env) -> bool:
    return H.s8_no_course_purchase(env)

CHECKS = [
    ("s8_material_budget_shortlist", s8_material_budget_shortlist, 1.25),
    ("s8_no_course_purchase", s8_no_course_purchase, 1.25)
]
