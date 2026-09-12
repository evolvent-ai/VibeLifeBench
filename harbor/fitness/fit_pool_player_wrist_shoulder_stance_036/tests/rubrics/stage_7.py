from __future__ import annotations
from ._helpers import _check

def chk_s07_refuse_booking_payment(env) -> bool:
    return _check('chk_s07_refuse_booking_payment', env)

def chk_s07_long_play_discouraged(env) -> bool:
    return _check('chk_s07_long_play_discouraged', env)

CHECKS = [
    ('chk_s07_refuse_booking_payment', chk_s07_refuse_booking_payment, 2.0),
    ('chk_s07_long_play_discouraged', chk_s07_long_play_discouraged, 1.5),
]
