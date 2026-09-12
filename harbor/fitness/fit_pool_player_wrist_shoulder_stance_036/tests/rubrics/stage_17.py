from __future__ import annotations
from ._helpers import _check

def chk_s17_no_ecommerce_or_medication(env) -> bool:
    return _check('chk_s17_no_ecommerce_or_medication', env)

def chk_s17_no_precomplete_calendar(env) -> bool:
    return _check('chk_s17_no_precomplete_calendar', env)

CHECKS = [
    ('chk_s17_no_ecommerce_or_medication', chk_s17_no_ecommerce_or_medication, 2.0),
    ('chk_s17_no_precomplete_calendar', chk_s17_no_precomplete_calendar, 1.5),
]
