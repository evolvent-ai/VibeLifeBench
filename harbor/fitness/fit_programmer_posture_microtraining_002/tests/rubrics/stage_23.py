from __future__ import annotations
from ._helpers import _check

def chk_s23_reject_hr_camp(env) -> bool:
    return _check('chk_s23_reject_hr_camp', env)

CHECKS = [
    ('chk_s23_reject_hr_camp', chk_s23_reject_hr_camp, 2),
]
