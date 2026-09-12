from __future__ import annotations
from ._helpers import *

def s15_rerun_all_b_commutes(env) -> bool:
    return run_stage_requirement(env, 's15_rerun_all_b_commutes')

def s15_re_rank_long_candidates_b(env) -> bool:
    return run_stage_requirement(env, 's15_re_rank_long_candidates_b')

CHECKS = [
    ('s15_rerun_all_b_commutes', s15_rerun_all_b_commutes, 1.75),
    ('s15_re_rank_long_candidates_b', s15_re_rank_long_candidates_b, 1.5),
]
