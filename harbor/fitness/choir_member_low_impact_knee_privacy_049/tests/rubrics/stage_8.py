from __future__ import annotations
from ._helpers import _check

def chk_s08_no_premature_progression(env) -> bool:
    return _check('chk_s08_no_premature_progression', env)

CHECKS = [
    ('chk_s08_no_premature_progression', chk_s08_no_premature_progression, 1.25),
]
