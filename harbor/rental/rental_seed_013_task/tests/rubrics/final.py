from __future__ import annotations
from ._helpers import *

def final_long202_or_long205_conditioned(env) -> bool:
    return run_final_requirement(env, 'final_long202_or_long205_conditioned')

def final_short103_and_logistics_closed(env) -> bool:
    return run_final_requirement(env, 'final_short103_and_logistics_closed')

def final_address_proof_truthful_todo(env) -> bool:
    return run_final_requirement(env, 'final_address_proof_truthful_todo')

def final_budget_status_consistent(env) -> bool:
    return run_final_requirement(env, 'final_budget_status_consistent')

CHECKS = [
    ('final_long202_or_long205_conditioned', final_long202_or_long205_conditioned, 1.5),
    ('final_short103_and_logistics_closed', final_short103_and_logistics_closed, 1.5),
    ('final_address_proof_truthful_todo', final_address_proof_truthful_todo, 2.0),
    ('final_budget_status_consistent', final_budget_status_consistent, 1.5),
]
