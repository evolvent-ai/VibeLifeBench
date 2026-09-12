from __future__ import annotations
from ._helpers import _check

def chk_s27_final_review_complete(env) -> bool:
    return _check('chk_s27_final_review_complete', env)

def chk_cb_s27_final_refresh_floor(env) -> bool:
    return _check('chk_cb_s27_final_refresh_floor', env)

def chk_cb_pro_s27_final_five_service_refresh(env) -> bool:
    return _check('chk_cb_pro_s27_final_five_service_refresh', env)

def chk_cb_pro_s27_final_three_service_handoff(env) -> bool:
    return _check('chk_cb_pro_s27_final_three_service_handoff', env)

def chk_cb_pro_s27_final_two_service_handoff(env) -> bool:
    return _check('chk_cb_pro_s27_final_two_service_handoff', env)

CHECKS = [
    ('chk_s27_final_review_complete', chk_s27_final_review_complete, 1.75),
    ('chk_cb_s27_final_refresh_floor', chk_cb_s27_final_refresh_floor, 1.25),
    ('chk_cb_pro_s27_final_five_service_refresh', chk_cb_pro_s27_final_five_service_refresh, 1.25),
    ('chk_cb_pro_s27_final_three_service_handoff', chk_cb_pro_s27_final_three_service_handoff, 1.0),
    ('chk_cb_pro_s27_final_two_service_handoff', chk_cb_pro_s27_final_two_service_handoff, 1.0),
]
