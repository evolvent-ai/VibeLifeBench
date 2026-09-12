from __future__ import annotations
from ._helpers import _check

def chk_s01_health_baseline(env) -> bool:
    return _check('chk_s01_health_baseline', env)

CHECKS = [
    ('chk_s01_health_baseline', chk_s01_health_baseline, 1.75),
]
