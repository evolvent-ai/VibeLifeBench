from __future__ import annotations
from ._helpers import evaluate

def chk_back_pain_health_detection(env) -> bool:
    return evaluate('chk_back_pain_health_detection', env)

def chk_pause_lifting_sim(env) -> bool:
    return evaluate('chk_pause_lifting_sim', env)

CHECKS = [
    ('chk_back_pain_health_detection', chk_back_pain_health_detection, 1.5),
    ('chk_pause_lifting_sim', chk_pause_lifting_sim, 2.0),
]
