from __future__ import annotations
from ._helpers import _check

def chk_s24_review_risk_propagated(env) -> bool:
    return _check('chk_s24_review_risk_propagated', env)

def chk_s24_diff_exclusion_file_lite(env) -> bool:
    return _check('chk_s24_diff_exclusion_file_lite', env)

CHECKS = [
    ('chk_s24_review_risk_propagated', chk_s24_review_risk_propagated, 1.5),
    ('chk_s24_diff_exclusion_file_lite', chk_s24_diff_exclusion_file_lite, 1.0),
]
