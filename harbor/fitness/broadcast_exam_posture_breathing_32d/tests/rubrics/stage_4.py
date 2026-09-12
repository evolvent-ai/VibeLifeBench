from __future__ import annotations
from ._helpers import evaluate

def chk_s04_cold_warmup_adjust(env) -> bool:
    return evaluate('chk_s04_cold_warmup_adjust', env)

CHECKS = [
    ('chk_s04_cold_warmup_adjust', chk_s04_cold_warmup_adjust, 1.5),
]
