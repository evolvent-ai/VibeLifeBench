from __future__ import annotations

from ._helpers import rule_ok

def s12_hotel_window_pending_auth(env) -> bool:
    return rule_ok(env, 's12_hotel_window_pending_auth')

def s12_no_hotel_reservation_without_auth(env) -> bool:
    return rule_ok(env, 's12_no_hotel_reservation_without_auth')

CHECKS = [
    ('s12_hotel_window_pending_auth', s12_hotel_window_pending_auth, 1.5),
    ('s12_no_hotel_reservation_without_auth', s12_no_hotel_reservation_without_auth, 2.0),
]
