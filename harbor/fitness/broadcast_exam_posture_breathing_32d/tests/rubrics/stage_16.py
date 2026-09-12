from __future__ import annotations
from ._helpers import evaluate

def chk_s16_voice_fatigue_response(env) -> bool:
    return evaluate('chk_s16_voice_fatigue_response', env)

CHECKS = [
    ('chk_s16_voice_fatigue_response', chk_s16_voice_fatigue_response, 2.0),
]
