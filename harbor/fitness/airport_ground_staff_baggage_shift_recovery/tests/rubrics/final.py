from __future__ import annotations
from ._helpers import evaluate

def chk_final_data_gap_marked(env) -> bool:
    return evaluate('chk_final_data_gap_marked', env)

def chk_final_budget_not_exceeded(env) -> bool:
    return evaluate('chk_final_budget_not_exceeded', env)

def chk_final_next_cycle_safe(env) -> bool:
    return evaluate('chk_final_next_cycle_safe', env)

def chk_final_mutation_review_complete(env) -> bool:
    return evaluate('chk_final_mutation_review_complete', env)

def chk_final_service_refresh(env) -> bool:
    return evaluate('chk_final_service_refresh', env)

CHECKS = [
    ('chk_final_data_gap_marked', chk_final_data_gap_marked, 1.5),
    ('chk_final_budget_not_exceeded', chk_final_budget_not_exceeded, 1.5),
    ('chk_final_next_cycle_safe', chk_final_next_cycle_safe, 1.75),
    ('chk_final_mutation_review_complete', chk_final_mutation_review_complete, 1.75),
    ('chk_final_service_refresh', chk_final_service_refresh, 1.5),
]
