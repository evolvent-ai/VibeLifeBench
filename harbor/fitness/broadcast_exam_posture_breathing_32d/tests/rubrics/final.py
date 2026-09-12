from __future__ import annotations
from ._helpers import evaluate

def chk_final_review_causal(env) -> bool:
    return evaluate('chk_final_review_causal', env)

def chk_final_next_cycle(env) -> bool:
    return evaluate('chk_final_next_cycle', env)

def chk_final_budget_auth_clean(env) -> bool:
    return evaluate('chk_final_budget_auth_clean', env)

def chk_final_package_ids_consistent(env) -> bool:
    return evaluate('chk_final_package_ids_consistent', env)

CHECKS = [
    ('chk_final_review_causal', chk_final_review_causal, 2.0),
    ('chk_final_next_cycle', chk_final_next_cycle, 1.5),
    ('chk_final_budget_auth_clean', chk_final_budget_auth_clean, 1.5),
    ('chk_final_package_ids_consistent', chk_final_package_ids_consistent, 1.0),
]
