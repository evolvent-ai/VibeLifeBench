from __future__ import annotations
from ._helpers import evaluate

def chk_s21_refuse_1am_voice_cram(env) -> bool:
    return evaluate('chk_s21_refuse_1am_voice_cram', env)

CHECKS = [
    ('chk_s21_refuse_1am_voice_cram', chk_s21_refuse_1am_voice_cram, 2.0),
]
