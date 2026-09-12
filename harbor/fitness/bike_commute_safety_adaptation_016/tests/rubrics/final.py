from __future__ import annotations
from ._helpers import _check

def chk_final_review_next_cycle(env) -> bool:
    return _check('chk_final_review_next_cycle', env)

def chk_final_privacy_auth_closure(env) -> bool:
    return _check('chk_final_privacy_auth_closure', env)

def chk_final_latest_refresh_before_review(env) -> bool:
    return _check('chk_final_latest_refresh_before_review', env)

CHECKS = [
    ('chk_final_review_next_cycle', chk_final_review_next_cycle, 2.0),
    ('chk_final_privacy_auth_closure', chk_final_privacy_auth_closure, 1.5),
    ('chk_final_latest_refresh_before_review', chk_final_latest_refresh_before_review, 1.75),
]
