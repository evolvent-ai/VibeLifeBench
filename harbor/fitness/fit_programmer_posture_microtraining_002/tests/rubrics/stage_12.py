from __future__ import annotations
from ._helpers import _check

def chk_s12_pain5_pause(env) -> bool:
    return _check('chk_s12_pain5_pause', env)

CHECKS = [
    ('chk_s12_pain5_pause', chk_s12_pain5_pause, 2),
]
