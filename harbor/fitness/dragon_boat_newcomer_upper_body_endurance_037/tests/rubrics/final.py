from __future__ import annotations
from ._helpers import _check

def chk_final_auth_statement(env) -> bool:
    return _check('chk_final_auth_statement', env)

def chk_final_next_cycle_plan(env) -> bool:
    return _check('chk_final_next_cycle_plan', env)

def chk_final_latest_refresh(env) -> bool:
    return _check('chk_final_latest_refresh', env)

CHECKS = [
    ('chk_final_auth_statement', chk_final_auth_statement, 1.5),
    ('chk_final_next_cycle_plan', chk_final_next_cycle_plan, 1.25),
    ('chk_final_latest_refresh', chk_final_latest_refresh, 1.75)
]
