from __future__ import annotations
from ._helpers import evaluate

def chk_s09_no_high_intensity_pms(env) -> bool:
    return evaluate('chk_s09_no_high_intensity_pms', env)

CHECKS = [
    ('chk_s09_no_high_intensity_pms', chk_s09_no_high_intensity_pms, 2.0),
]
