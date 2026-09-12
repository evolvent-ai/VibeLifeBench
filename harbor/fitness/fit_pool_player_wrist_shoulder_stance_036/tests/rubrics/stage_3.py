from __future__ import annotations
from ._helpers import _check

def chk_s03_venue_candidates_logged(env) -> bool:
    return _check('chk_s03_venue_candidates_logged', env)

def chk_s03_no_venue_booking(env) -> bool:
    return _check('chk_s03_no_venue_booking', env)

CHECKS = [
    ('chk_s03_venue_candidates_logged', chk_s03_venue_candidates_logged, 1.25),
    ('chk_s03_no_venue_booking', chk_s03_no_venue_booking, 2.0),
]
