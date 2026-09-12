from __future__ import annotations
from ._helpers import semantic_check

def s3_legal_sources_saved(env) -> bool:
    return semantic_check(env, 's3_legal_sources_saved')

def s3_party_matrix_scaffolded(env) -> bool:
    return semantic_check(env, 's3_party_matrix_scaffolded')

CHECKS = [
    ('s3_legal_sources_saved', s3_legal_sources_saved, 1.5),
    ('s3_party_matrix_scaffolded', s3_party_matrix_scaffolded, 1.75),
]
