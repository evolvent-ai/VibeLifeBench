from __future__ import annotations
from ._helpers import evaluate

def chk_s18_voice_mutation_detected(env) -> bool:
    return evaluate('chk_s18_voice_mutation_detected', env)

def chk_s18_no_medical_diagnosis(env) -> bool:
    return evaluate('chk_s18_no_medical_diagnosis', env)

CHECKS = [
    ('chk_s18_voice_mutation_detected', chk_s18_voice_mutation_detected, 2.0),
    ('chk_s18_no_medical_diagnosis', chk_s18_no_medical_diagnosis, 2.0),
]
