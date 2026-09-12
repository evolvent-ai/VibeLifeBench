from __future__ import annotations
from ._helpers import semantic_check

def final_handoff_status_complete(env) -> bool:
    return semantic_check(env, 'final_handoff_status_complete')

CHECKS = [
    ('final_handoff_status_complete', final_handoff_status_complete, 1.75),
]
