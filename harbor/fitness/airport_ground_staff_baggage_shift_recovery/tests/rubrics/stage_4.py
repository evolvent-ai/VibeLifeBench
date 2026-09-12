from __future__ import annotations
from ._helpers import evaluate

def chk_scheduled_checks_created(env) -> bool:
    return evaluate('chk_scheduled_checks_created', env)

CHECKS = [
    ('chk_scheduled_checks_created', chk_scheduled_checks_created, 1.5),
]
