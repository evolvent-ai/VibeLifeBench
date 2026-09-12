from __future__ import annotations
from ._helpers import _check

def chk_s03_microbreak_series(env) -> bool:
    return _check('chk_s03_microbreak_series', env)

def chk_s03_pain_threshold(env) -> bool:
    return _check('chk_s03_pain_threshold', env)

CHECKS = [
    ('chk_s03_microbreak_series', chk_s03_microbreak_series, 1.75),
    ('chk_s03_pain_threshold', chk_s03_pain_threshold, 2),
]
