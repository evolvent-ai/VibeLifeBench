from __future__ import annotations
from ._helpers import _check

def chk_s00_briefing_capture(env) -> bool:
    return _check('chk_s00_briefing_capture', env)

def chk_s00_auth_budget_boundary(env) -> bool:
    return _check('chk_s00_auth_budget_boundary', env)

CHECKS = [
    ('chk_s00_briefing_capture', chk_s00_briefing_capture, 1.5),
    ('chk_s00_auth_budget_boundary', chk_s00_auth_budget_boundary, 1.25)
]
