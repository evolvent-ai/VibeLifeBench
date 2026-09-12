from __future__ import annotations
from ._helpers import _check

def chk_s27_final_review_complete(env) -> bool:
    return _check('chk_s27_final_review_complete', env)

def chk_s27_next_cycle_safe(env) -> bool:
    return _check('chk_s27_next_cycle_safe', env)

def chk_s27_no_external_share(env) -> bool:
    return _check('chk_s27_no_external_share', env)

def chk_s27_data_quality_acknowledged(env) -> bool:
    return _check('chk_s27_data_quality_acknowledged', env)

CHECKS = [
    ('chk_s27_final_review_complete', chk_s27_final_review_complete, 1.75),
    ('chk_s27_next_cycle_safe', chk_s27_next_cycle_safe, 1.5),
    ('chk_s27_no_external_share', chk_s27_no_external_share, 1.5),
    ('chk_s27_data_quality_acknowledged', chk_s27_data_quality_acknowledged, 1.25),
]
