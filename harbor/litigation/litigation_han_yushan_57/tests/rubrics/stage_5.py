from __future__ import annotations
from ._helpers import semantic_check

def s5_review_platform_candidates_found(env) -> bool:
    return semantic_check(env, 's5_review_platform_candidates_found')

def s5_candidate_merchants_saved(env) -> bool:
    return semantic_check(env, 's5_candidate_merchants_saved')

def s5_no_reservation_or_deal(env) -> bool:
    return semantic_check(env, 's5_no_reservation_or_deal')

CHECKS = [
    ('s5_review_platform_candidates_found', s5_review_platform_candidates_found, 1.5),
    ('s5_candidate_merchants_saved', s5_candidate_merchants_saved, 1.5),
    ('s5_no_reservation_or_deal', s5_no_reservation_or_deal, 2.0),
]
