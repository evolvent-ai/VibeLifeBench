from __future__ import annotations
from ._helpers import check_s1_book_viable_bj_to_suz, check_s1_low_disturbance_uncle

def s1_book_viable_bj_to_suz(env) -> bool:
    return check_s1_book_viable_bj_to_suz(env)

def s1_low_disturbance_uncle(env) -> bool:
    return check_s1_low_disturbance_uncle(env)

CHECKS = [
    ("s1_book_viable_bj_to_suz", s1_book_viable_bj_to_suz, 1.5),
    ("s1_low_disturbance_uncle", s1_low_disturbance_uncle, 1.5),
]
