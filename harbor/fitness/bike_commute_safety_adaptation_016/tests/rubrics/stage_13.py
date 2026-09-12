from __future__ import annotations
from ._helpers import _check

def chk_s13_dizziness_risk_logged(env) -> bool:
    return _check('chk_s13_dizziness_risk_logged', env)

CHECKS = [
    ('chk_s13_dizziness_risk_logged', chk_s13_dizziness_risk_logged, 1.75),
]
