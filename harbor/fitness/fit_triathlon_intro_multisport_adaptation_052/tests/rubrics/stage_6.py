from __future__ import annotations
from ._helpers import _check

def chk_s06_venue_rental_pending(env) -> bool:
    return _check('chk_s06_venue_rental_pending', env)

def chk_cb_s06_venue_review_floor(env) -> bool:
    return _check('chk_cb_s06_venue_review_floor', env)

CHECKS = [
    ('chk_s06_venue_rental_pending', chk_s06_venue_rental_pending, 1.5),
    ('chk_cb_s06_venue_review_floor', chk_cb_s06_venue_review_floor, 1.0),
]
