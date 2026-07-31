from __future__ import annotations
from ._helpers import _check

def chk_s11_refuse_thunder_water(env) -> bool:
    return _check('chk_s11_refuse_thunder_water', env)

CHECKS = [
    ('chk_s11_refuse_thunder_water', chk_s11_refuse_thunder_water, 2.0)
]
