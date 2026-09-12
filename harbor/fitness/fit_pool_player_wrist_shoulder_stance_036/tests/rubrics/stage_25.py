from __future__ import annotations
from ._helpers import _check

def chk_s25_club_hours_detected(env) -> bool:
    return _check('chk_s25_club_hours_detected', env)

def chk_s25_short_walkin_plan(env) -> bool:
    return _check('chk_s25_short_walkin_plan', env)

CHECKS = [
    ('chk_s25_club_hours_detected', chk_s25_club_hours_detected, 1.5),
    ('chk_s25_short_walkin_plan', chk_s25_short_walkin_plan, 1.75),
]
