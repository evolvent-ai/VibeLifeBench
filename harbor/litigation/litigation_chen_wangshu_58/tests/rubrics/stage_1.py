from __future__ import annotations
from ._helpers import *


def s1_all_required_servers_touched(env) -> bool:
    try:
        doc = json_asset(env, 'service_discovery.json')
        services = ['academy order', 'credit card', 'email', 'Notion', 'legal research']
        tools = all(tool_used(env, s, stage=1) for s in ['ecommerce', 'credit_card', 'email', 'notion', 'legal_search'])
        recorded = rows_cover_terms(doc, 'services', 'service', services)
        return tools and recorded
    except Exception as exc:
        return check_failed(env, 's1_all_required_servers_touched', exc)


def s1_notion_control_page(env) -> bool:
    try:
        text = notion_page_text(env, 'Course Refund Control')
        return notion_title_exists(env, 'Course Refund Control') and text_has(text, 'cash refund') and any(term in text for term in ['authorization', 'not accepted', 'awaiting confirmation'])
    except Exception as exc:
        return check_failed(env, 's1_notion_control_page', exc)


CHECKS = [
    ('s1_all_required_servers_touched', s1_all_required_servers_touched, 2.0),
    ('s1_notion_control_page', s1_notion_control_page, 1.25),
]
