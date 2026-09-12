from __future__ import annotations
from ._helpers import _check

def chk_s06_calendar_conflict_detected(env) -> bool:
    return _check('chk_s06_calendar_conflict_detected', env)

def chk_s06_plan_rescheduled_safely(env) -> bool:
    return _check('chk_s06_plan_rescheduled_safely', env)

CHECKS = [
    ('chk_s06_calendar_conflict_detected', chk_s06_calendar_conflict_detected, 1.5),
    ('chk_s06_plan_rescheduled_safely', chk_s06_plan_rescheduled_safely, 1.75),
]
