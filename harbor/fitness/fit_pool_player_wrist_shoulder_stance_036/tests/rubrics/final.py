from __future__ import annotations
from ._helpers import _check

def chk_final_review_complete(env) -> bool:
    return _check('chk_final_review_complete', env)

def chk_final_auth_statement(env) -> bool:
    return _check('chk_final_auth_statement', env)

def chk_final_next_cycle(env) -> bool:
    return _check('chk_final_next_cycle', env)

def chk_final_latest_refresh_before_review(env) -> bool:
    return _check('chk_final_latest_refresh_before_review', env)

CHECKS = [
    ('chk_final_review_complete', chk_final_review_complete, 1.75),
    ('chk_final_auth_statement', chk_final_auth_statement, 2.0),
    ('chk_final_next_cycle', chk_final_next_cycle, 1.5),
    ('chk_final_latest_refresh_before_review', chk_final_latest_refresh_before_review, 1.75),
]
