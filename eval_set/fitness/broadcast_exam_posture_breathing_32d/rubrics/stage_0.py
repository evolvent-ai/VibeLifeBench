from __future__ import annotations
from ._helpers import evaluate

def chk_s00_briefing_constraints(env) -> bool:
    return evaluate('chk_s00_briefing_constraints', env)

def chk_s00_notion_hub_init(env) -> bool:
    return evaluate('chk_s00_notion_hub_init', env)

CHECKS = [
    ('chk_s00_briefing_constraints', chk_s00_briefing_constraints, 2.0),
    ('chk_s00_notion_hub_init', chk_s00_notion_hub_init, 1.25),
]
