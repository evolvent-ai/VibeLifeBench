from __future__ import annotations
from ._helpers import _check

def chk_s07_load_progression_one_variable(env) -> bool:
    return _check('chk_s07_load_progression_one_variable', env)

CHECKS = [
    ('chk_s07_load_progression_one_variable', chk_s07_load_progression_one_variable, 1.5),
]
