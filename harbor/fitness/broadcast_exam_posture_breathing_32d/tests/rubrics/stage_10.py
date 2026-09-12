from __future__ import annotations
from ._helpers import evaluate

def chk_s10_gradual_restore(env) -> bool:
    return evaluate('chk_s10_gradual_restore', env)

CHECKS = [
    ('chk_s10_gradual_restore', chk_s10_gradual_restore, 1.5),
]
