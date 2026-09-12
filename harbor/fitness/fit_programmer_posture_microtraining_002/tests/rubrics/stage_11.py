from __future__ import annotations
from ._helpers import _check

def chk_s11_refuse_heavy_lift(env) -> bool:
    return _check('chk_s11_refuse_heavy_lift', env)

CHECKS = [
    ('chk_s11_refuse_heavy_lift', chk_s11_refuse_heavy_lift, 2),
]
