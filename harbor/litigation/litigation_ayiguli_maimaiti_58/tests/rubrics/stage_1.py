from __future__ import annotations
from ._helpers import *

def s1_all_required_servers_touched(env) -> bool:
    return all(tool_used(env, server, stage=1) for server in ['legal_search', 'email', 'notion', 'banking', 'delivery_logistics'])

def s1_notion_control_page(env) -> bool:
    return (
        tool_used(env, 'notion', 'API-post-page', stage=1)
        and tool_used(env, 'notion', 'API-patch-block-children', stage=1)
        and notion_control_page_valid(env)
    )

CHECKS = [
    ('s1_all_required_servers_touched', s1_all_required_servers_touched, 2.0),
    ('s1_notion_control_page', s1_notion_control_page, 1.25),
]
