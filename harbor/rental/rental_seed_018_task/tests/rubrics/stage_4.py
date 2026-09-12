from __future__ import annotations
from ._helpers import *

def s4_review_risk_sources(env) -> bool:
    return (
        tool_stage(env, 4, 'review_platform', None, [C.MER_B])
        and tool_stage(env, 4, 'review_platform', None, [C.MER_C])
        and s4_risk_page_update(env)
    )

def s4_risk_page_update(env) -> bool:
    return (
        tool_stage(env, 4, 'notion', None, [C.LIST_B])
        and notion_has_parts(env, [C.LIST_B])
        and tool_stage(env, 4, 'listing_platform', None, [C.LIST_B])
    )

CHECKS = [
    ('s4_review_risk_sources', s4_review_risk_sources, 1.5),
    ('s4_risk_page_update', s4_risk_page_update, 1.25),
]
