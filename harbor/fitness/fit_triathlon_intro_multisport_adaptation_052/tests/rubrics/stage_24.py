from __future__ import annotations
from ._helpers import _check

def chk_s24_taper_no_hard_brick(env) -> bool:
    return _check('chk_s24_taper_no_hard_brick', env)

CHECKS = [
    ('chk_s24_taper_no_hard_brick', chk_s24_taper_no_hard_brick, 2.0),
]
