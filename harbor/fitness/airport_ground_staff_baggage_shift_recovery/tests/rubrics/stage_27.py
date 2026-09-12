from __future__ import annotations
from ._helpers import evaluate

def chk_stage27_closure_handoff(env) -> bool:
    return evaluate('chk_stage27_closure_handoff', env)

CHECKS = [
    ('chk_stage27_closure_handoff', chk_stage27_closure_handoff, 1.75),
]
