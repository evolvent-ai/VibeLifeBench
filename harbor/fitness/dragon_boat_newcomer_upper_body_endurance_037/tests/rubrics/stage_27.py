from __future__ import annotations
from ._helpers import _check

def chk_s27_final_review_complete(env) -> bool:
    return _check('chk_s27_final_review_complete', env)

CHECKS = [
    ('chk_s27_final_review_complete', chk_s27_final_review_complete, 2.0)
]
