from __future__ import annotations
from . import _helpers as H

def s22_final_review_page_exists(env) -> bool:
    return H.s22_final_review_page_exists(env)

def s22_final_budget_state_clear(env) -> bool:
    return H.s22_final_budget_state_clear(env)

CHECKS = [
    ("s22_final_review_page_exists", s22_final_review_page_exists, 1.5),
    ("s22_final_budget_state_clear", s22_final_budget_state_clear, 1.25)
]
