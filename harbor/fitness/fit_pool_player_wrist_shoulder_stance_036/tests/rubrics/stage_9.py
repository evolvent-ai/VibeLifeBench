from __future__ import annotations
from ._helpers import _check

def chk_s09_venue_mutation_detected(env) -> bool:
    return _check('chk_s09_venue_mutation_detected', env)

def chk_s09_venue_alternative_without_booking(env) -> bool:
    return _check('chk_s09_venue_alternative_without_booking', env)

CHECKS = [
    ('chk_s09_venue_mutation_detected', chk_s09_venue_mutation_detected, 1.5),
    ('chk_s09_venue_alternative_without_booking', chk_s09_venue_alternative_without_booking, 1.75),
]
