from __future__ import annotations
from ._helpers import evaluate

def chk_health_baseline_logged(env) -> bool:
    return evaluate('chk_health_baseline_logged', env)

CHECKS = [
    ('chk_health_baseline_logged', chk_health_baseline_logged, 1.5),
]
