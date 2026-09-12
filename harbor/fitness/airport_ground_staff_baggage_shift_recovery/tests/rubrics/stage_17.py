from __future__ import annotations
from ._helpers import evaluate

def chk_risk_log_professional_eval(env) -> bool:
    return evaluate('chk_risk_log_professional_eval', env)

CHECKS = [
    ('chk_risk_log_professional_eval', chk_risk_log_professional_eval, 1.5),
]
