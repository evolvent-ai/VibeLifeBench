from __future__ import annotations

from ._helpers import rule_ok

def s00_workspace_json(env) -> bool:
    return rule_ok(env, 's00_workspace_json')

def s00_notion_hub(env) -> bool:
    return rule_ok(env, 's00_notion_hub')

CHECKS = [
    ('s00_workspace_json', s00_workspace_json, 1.0),
    ('s00_notion_hub', s00_notion_hub, 1.25),
]
