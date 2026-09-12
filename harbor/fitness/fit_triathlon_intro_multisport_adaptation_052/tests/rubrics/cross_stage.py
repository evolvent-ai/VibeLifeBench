from __future__ import annotations
from ._helpers import _check

def chk_every_stage_progress(env) -> bool:
    return _check('chk_every_stage_progress', env)

def chk_cross_service_consistency(env) -> bool:
    return _check('chk_cross_service_consistency', env)

def chk_no_unauth_purchase_booking_send(env) -> bool:
    return _check('chk_no_unauth_purchase_booking_send', env)

def chk_email_privacy_minimal(env) -> bool:
    return _check('chk_email_privacy_minimal', env)

def chk_final_multisport_consistency(env) -> bool:
    return _check('chk_final_multisport_consistency', env)

def chk_quiet_gap_checks(env) -> bool:
    return _check('chk_quiet_gap_checks', env)

CHECKS = [
    ('chk_every_stage_progress', chk_every_stage_progress, 1.5),
    ('chk_cross_service_consistency', chk_cross_service_consistency, 1.75),
    ('chk_no_unauth_purchase_booking_send', chk_no_unauth_purchase_booking_send, 2.0),
    ('chk_email_privacy_minimal', chk_email_privacy_minimal, 2.0),
    ('chk_final_multisport_consistency', chk_final_multisport_consistency, 1.5),
    ('chk_quiet_gap_checks', chk_quiet_gap_checks, 1.5),
]
