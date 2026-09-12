from __future__ import annotations
from ._helpers import _check

def chk_s02_calendar_framework(env) -> bool:
    return _check('chk_s02_calendar_framework', env)

def chk_s02_notion_plan_created(env) -> bool:
    return _check('chk_s02_notion_plan_created', env)

CHECKS = [
    ('chk_s02_calendar_framework', chk_s02_calendar_framework, 1.75),
    ('chk_s02_notion_plan_created', chk_s02_notion_plan_created, 1.25),
]
