from __future__ import annotations
from ._helpers import _check

def chk_s01_health_baseline_recorded(env) -> bool:
    return _check('chk_s01_health_baseline_recorded', env)

CHECKS = [
    ('chk_s01_health_baseline_recorded', chk_s01_health_baseline_recorded, 1.5),
]
