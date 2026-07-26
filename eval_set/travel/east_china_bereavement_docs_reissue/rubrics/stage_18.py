from __future__ import annotations
from ._helpers import check_s18_gate_update

def s18_gate_update(env) -> bool:
    return check_s18_gate_update(env)

CHECKS = [
    ("s18_gate_update", s18_gate_update, 2),
]
