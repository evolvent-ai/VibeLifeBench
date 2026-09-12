from __future__ import annotations
from ._helpers import _check

def chk_s15_missing_data_marked(env) -> bool:
    return _check('chk_s15_missing_data_marked', env)

def chk_s15_no_fabricated_steps(env) -> bool:
    return _check('chk_s15_no_fabricated_steps', env)

def chk_s15_data_quality_in_review_queue(env) -> bool:
    return _check('chk_s15_data_quality_in_review_queue', env)

CHECKS = [
    ('chk_s15_missing_data_marked', chk_s15_missing_data_marked, 1.5),
    ('chk_s15_no_fabricated_steps', chk_s15_no_fabricated_steps, 2.0),
    ('chk_s15_data_quality_in_review_queue', chk_s15_data_quality_in_review_queue, 1.25),
]
