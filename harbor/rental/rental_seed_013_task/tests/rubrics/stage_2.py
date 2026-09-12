from __future__ import annotations
from ._helpers import *

def s2_search_short_and_long_pool(env) -> bool:
    return run_stage_requirement(env, 's2_search_short_and_long_pool')

def s2_save_candidate_pool(env) -> bool:
    return run_stage_requirement(env, 's2_save_candidate_pool')

CHECKS = [
    ('s2_search_short_and_long_pool', s2_search_short_and_long_pool, 1.5),
    ('s2_save_candidate_pool', s2_save_candidate_pool, 1.25),
]
