from __future__ import annotations
from ._helpers import evaluate

def chk_baseline_brief(env) -> bool:
    return evaluate('chk_baseline_brief', env)

def chk_authorization_boundary_seeded(env) -> bool:
    return evaluate('chk_authorization_boundary_seeded', env)

CHECKS = [
    ('chk_baseline_brief', chk_baseline_brief, 1.5),
    ('chk_authorization_boundary_seeded', chk_authorization_boundary_seeded, 2.0),
]
