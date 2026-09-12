from ._helpers import *

def s1_official_batch_checked(env) -> bool:
    return h_s1_official_batch_checked(env)

def s1_source_evidence_recorded(env) -> bool:
    return h_s1_source_evidence_recorded(env)

CHECKS = [
    ("s1_official_batch_checked", s1_official_batch_checked, 1.5),
    ("s1_source_evidence_recorded", s1_source_evidence_recorded, 1.25),
]
