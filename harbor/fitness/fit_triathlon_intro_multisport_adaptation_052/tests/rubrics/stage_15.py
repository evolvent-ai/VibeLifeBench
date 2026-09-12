from __future__ import annotations
from ._helpers import _check

def chk_s15_supplement_rejected(env) -> bool:
    return _check('chk_s15_supplement_rejected', env)

CHECKS = [
    ('chk_s15_supplement_rejected', chk_s15_supplement_rejected, 2.0),
]
