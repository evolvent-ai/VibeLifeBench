from __future__ import annotations
from ._helpers import evaluate

def chk_back_pain_user_reply(env) -> bool:
    return evaluate('chk_back_pain_user_reply', env)

CHECKS = [
    ('chk_back_pain_user_reply', chk_back_pain_user_reply, 2.0),
]
