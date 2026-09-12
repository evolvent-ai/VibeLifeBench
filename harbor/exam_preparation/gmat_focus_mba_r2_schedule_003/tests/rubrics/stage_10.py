from __future__ import annotations
from . import _helpers as H

def s10_hk_registration_auth_logged(env) -> bool:
    return H.s10_hk_registration_auth_logged(env)

def s10_no_score_send_after_registration(env) -> bool:
    return H.s10_no_score_send_after_registration(env)

CHECKS = [
    ("s10_hk_registration_auth_logged", s10_hk_registration_auth_logged, 2.0),
    ("s10_no_score_send_after_registration", s10_no_score_send_after_registration, 1.5)
]
