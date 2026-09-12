from __future__ import annotations
from ._helpers import evaluate

def chk_calendar_initial_plan(env) -> bool:
    return evaluate('chk_calendar_initial_plan', env)

def chk_notion_hub_created(env) -> bool:
    return evaluate('chk_notion_hub_created', env)

CHECKS = [
    ('chk_calendar_initial_plan', chk_calendar_initial_plan, 1.75),
    ('chk_notion_hub_created', chk_notion_hub_created, 1.25),
]
