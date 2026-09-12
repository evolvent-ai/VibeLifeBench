from __future__ import annotations
from ._helpers import _check

def chk_s04_full_multisport_plan(env) -> bool:
    return _check('chk_s04_full_multisport_plan', env)

CHECKS = [
    ('chk_s04_full_multisport_plan', chk_s04_full_multisport_plan, 1.5),
]
