from __future__ import annotations
from ._helpers import _check

def chk_s04_initial_42d_plan(env) -> bool:
    return _check('chk_s04_initial_42d_plan', env)

def chk_s04_calendar_plan_seeded_light(env) -> bool:
    return _check('chk_s04_calendar_plan_seeded_light', env)

CHECKS = [
    ('chk_s04_initial_42d_plan', chk_s04_initial_42d_plan, 1.75),
    ('chk_s04_calendar_plan_seeded_light', chk_s04_calendar_plan_seeded_light, 1.0)
]
