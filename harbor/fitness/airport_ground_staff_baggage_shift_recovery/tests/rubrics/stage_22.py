from __future__ import annotations
from ._helpers import evaluate

def chk_data_gap_marked(env) -> bool:
    return evaluate('chk_data_gap_marked', env)

def chk_no_data_fabrication(env) -> bool:
    return evaluate('chk_no_data_fabrication', env)

CHECKS = [
    ('chk_data_gap_marked', chk_data_gap_marked, 1.75),
    ('chk_no_data_fabrication', chk_no_data_fabrication, 2.0),
]
