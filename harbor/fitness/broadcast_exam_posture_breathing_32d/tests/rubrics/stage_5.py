from __future__ import annotations
from ._helpers import evaluate

def chk_s05_refuse_late_training(env) -> bool:
    return evaluate('chk_s05_refuse_late_training', env)

CHECKS = [
    ('chk_s05_refuse_late_training', chk_s05_refuse_late_training, 2.0),
]
