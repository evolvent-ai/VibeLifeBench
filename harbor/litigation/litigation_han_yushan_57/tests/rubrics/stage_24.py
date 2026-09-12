from __future__ import annotations
from ._helpers import semantic_check

def s24_final_gap_party_candidate_complete(env) -> bool:
    return semantic_check(env, 's24_final_gap_party_candidate_complete')

CHECKS = [
    ('s24_final_gap_party_candidate_complete', s24_final_gap_party_candidate_complete, 1.75),
]
