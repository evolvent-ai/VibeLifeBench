from __future__ import annotations
from ._helpers import _check

def chk_s14_indoor_option_auth(env) -> bool:
    return _check('chk_s14_indoor_option_auth', env)

CHECKS = [
    ('chk_s14_indoor_option_auth', chk_s14_indoor_option_auth, 1.25)
]
