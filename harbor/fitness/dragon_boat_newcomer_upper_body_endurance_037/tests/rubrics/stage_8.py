from __future__ import annotations
from ._helpers import _check

def chk_s08_week1_completion_logged(env) -> bool:
    return _check('chk_s08_week1_completion_logged', env)

CHECKS = [
    ('chk_s08_week1_completion_logged', chk_s08_week1_completion_logged, 1.25)
]
