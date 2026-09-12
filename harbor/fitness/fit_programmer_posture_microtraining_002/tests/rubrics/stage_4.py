from __future__ import annotations
from ._helpers import _check

def chk_s04_venue_filter(env) -> bool:
    return _check('chk_s04_venue_filter', env)

CHECKS = [
    ('chk_s04_venue_filter', chk_s04_venue_filter, 1.5),
]
