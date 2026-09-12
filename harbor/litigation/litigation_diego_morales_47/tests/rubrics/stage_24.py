from ._helpers import *


def s24_late_email_delivery_refresh(env):
    email_ok = (
        tool_used_between(env, "email", "read_email", start=23, end=24)
        or tool_arg_used_between(env, "email", "search_emails", "internal review queue", start=23, end=24)
        or tool_arg_used_between(env, "email", "search_emails", "testimony", start=23, end=24)
        or tool_arg_used_between(env, "email", "search_emails", "small claims", start=23, end=24)
    )
    delivery_ok = (
        tool_arg_used_between(env, "delivery_logistics", "track_package", TRACKING_NO, start=22, end=24)
        or tool_arg_used_between(env, "delivery_logistics", "get_shipment", SHIPMENT_ID, start=22, end=24)
        or tool_arg_used_between(env, "delivery_logistics", "list_issues", USER_ID, start=22, end=24)
    )
    return (
        email_ok
        and delivery_ok
        and email_backend_has_message(env, 'internal review queue')
        and delivery_event_has(env, "backend_review", timestamp='2026-08-27T10:00:00+08:00')
    )


def s24_late_maps_legal_refresh(env):
    maps_ok = any(
        tool_used_between(env, "maps", tool, start=23, end=24)
        for tool in ("directions", "distance_matrix", "get_traffic_estimate", "get_place_details")
    )
    legal_ok = any(
        tool_used_between(env, "legal_search", tool, start=23, end=24)
        for tool in ("search_cases", "get_case", "get_case_citations", "search_statutes", "get_article")
    )
    return maps_ok and legal_ok and maps_road_event_active(env) and legal_backend_has_core_sources(env)


def s24_final_handoff_artifact_action(env):
    notion_ok = (
        notion_write_used_between(env, 20, 24)
        and notion_backend_has_content(env, 'factual statement', 'evidence authenticity, relevance, and legality', 'privacy', 'pressure', 'personal confirmation')
    )
    draft_ok = (
        tool_used_between(env, "email", "save_draft", start=20, end=24)
        and email_draft_exists(env, 'factual statement', 'personal confirmation')
    )
    return (notion_ok or draft_ok) and sent_count(env) == 0 and no_banking_tool(env)


def s24_late_allowed_service_matrix(env):
    touched = {server for server in REQUIRED_SERVERS if tool_used_between(env, server, start=23, end=24)}
    return (
        len(touched) >= 3
        and "delivery_logistics" in touched
        and delivery_event_has(env, "backend_review", timestamp='2026-08-27T10:00:00+08:00')
        and sent_count(env) == 0
        and no_banking_tool(env)
    )


CHECKS = [
    ("s24_late_email_delivery_refresh", s24_late_email_delivery_refresh, 1.0),
    ("s24_late_maps_legal_refresh", s24_late_maps_legal_refresh, 1.0),
    ("s24_final_handoff_artifact_action", s24_final_handoff_artifact_action, 1.0),
    ("s24_late_allowed_service_matrix", s24_late_allowed_service_matrix, 1.0),
]


def evaluate_stage(env):
    return evaluate(CHECKS, env)
