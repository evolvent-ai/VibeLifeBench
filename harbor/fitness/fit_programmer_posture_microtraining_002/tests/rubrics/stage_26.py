from __future__ import annotations
from ._helpers import _check

def chk_s25_cautious_progression(env) -> bool:
    return _check('chk_s25_cautious_progression', env)

def chk_s26_diff_cautious_calendar_lite(env) -> bool:
    return _check('chk_s26_diff_cautious_calendar_lite', env)

def chk_s26_diff_six_service_freshness(env) -> bool:
    return _check('chk_s26_diff_six_service_freshness', env)

CHECKS = [
    ('chk_s25_cautious_progression', chk_s25_cautious_progression, 1.75),
    ('chk_s26_diff_cautious_calendar_lite', chk_s26_diff_cautious_calendar_lite, 1.0),
    ('chk_s26_diff_six_service_freshness', chk_s26_diff_six_service_freshness, 1.25),
]
