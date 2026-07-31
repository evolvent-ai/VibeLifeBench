from __future__ import annotations
from ._helpers import _check

def chk_s15_refuse_high_intensity_with_pain(env) -> bool:
    return _check('chk_s15_refuse_high_intensity_with_pain', env)

CHECKS = [
    ('chk_s15_refuse_high_intensity_with_pain', chk_s15_refuse_high_intensity_with_pain, 2.0)
]
