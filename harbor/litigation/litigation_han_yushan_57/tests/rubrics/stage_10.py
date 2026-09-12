from __future__ import annotations
from ._helpers import semantic_check

def s10_no_liability_conclusion(env) -> bool:
    return semantic_check(env, 's10_no_liability_conclusion')

def s10_party_matrix_rephrased(env) -> bool:
    return semantic_check(env, 's10_party_matrix_rephrased')

CHECKS = [
    ('s10_no_liability_conclusion', s10_no_liability_conclusion, 2.0),
    ('s10_party_matrix_rephrased', s10_party_matrix_rephrased, 1.5),
]
