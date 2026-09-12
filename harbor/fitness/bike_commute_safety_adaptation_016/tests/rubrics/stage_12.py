from __future__ import annotations
from ._helpers import _check

def chk_s12_light_delay_no_night(env) -> bool:
    return _check('chk_s12_light_delay_no_night', env)

CHECKS = [
    ('chk_s12_light_delay_no_night', chk_s12_light_delay_no_night, 2.0),
]
