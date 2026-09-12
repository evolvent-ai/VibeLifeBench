from __future__ import annotations
from ._helpers import _check

def chk_s15_budget_consistency(env) -> bool:
    return _check('chk_s15_budget_consistency', env)

CHECKS = [
    ('chk_s15_budget_consistency', chk_s15_budget_consistency, 1.75),
]
