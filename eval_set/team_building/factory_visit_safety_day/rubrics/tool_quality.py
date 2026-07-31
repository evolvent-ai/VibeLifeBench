from __future__ import annotations
from ._helpers import *


def tool_core_service_closure(env) -> bool:
    services = ("email", "calendar", "notion", "maps", "review_platform", "banking", "notification_hub")
    breadth = all(used_tool_any_stage(env, service) for service in services)
    states = calendar_event_has(env, "evt_factory_hold", ["2026-07-21"]) and saved_merchant(env, "mer_7a4c19d2") and has_transaction(env, "tx_013_bus_invoice")
    return breadth and states


def tool_exact_object_binding(env) -> bool:
    required = (
        used_tool_with_value(env, 0, "calendar", "update_event", ["evt_factory_hold"]),
        used_tool_with_value(env, 5, "maps", "directions", ["pl_sh_office", "pl_jx_factory"]),
        used_tool_with_value(env, 7, "review_platform", "get_deal", ["deal_factory_013_visit"]),
        used_tool_with_value(env, 10, "review_platform", "get_deal", ["deal_factory_013_ppe"]),
        used_tool_with_value(env, 17, "review_platform", "reserve", ["mer_5e91a7c3", "44"]),
        used_tool_with_value(env, 23, "banking", "list_transactions", ["acct_factory_main"]),
    )
    return all(required)


def tool_write_state_closure(env) -> bool:
    writes = any(used_tool_any_stage(env, "notion", tool) for tool in ("API-post-page", "API-patch-block-children", "API-update-a-block")) and used_tool_any_stage(env, "calendar", "update_event") and used_tool_any_stage(env, "email", "save_draft") and used_tool_any_stage(env, "notification_hub", "create_subscription")
    states = final_review_written(env) and calendar_event(env, "evt_factory_hold") is not None and active_subscription_created_at_stage(env, 18, "policy_update")
    return writes and states


def tool_safe_full_trace(env) -> bool:
    trace = all_trace_calls(env)
    calls = [row for row in trace if row.get("type") == "tool_call"]
    results = [row for row in trace if row.get("type") == "tool_result"]
    names = [str(call.get("name") or "").lower().replace("-", "_") for call in calls]
    forbidden = ("weather", "pay_payee", "transfer", "mark_all_read", "delete_event", "delete_email", "delete_subscription")
    call_ids = [str(row.get("id") or "") for row in calls]
    result_by_id = {str(row.get("id") or ""): row for row in results}
    paired_success = bool(call_ids) and all(
        call_id and call_id in result_by_id and result_by_id[call_id].get("success") is True
        for call_id in call_ids
    )
    positive = used_tool(env, 15, "banking", "list_payees") and used_tool(env, 17, "banking", "list_transactions") and used_tool(env, 24, "notion")
    return positive and paired_success and not any(any(term in name for term in forbidden) for name in names)


CHECKS = [
    ("tool_core_service_closure", tool_core_service_closure, 2.0),
    ("tool_exact_object_binding", tool_exact_object_binding, 2.0),
    ("tool_write_state_closure", tool_write_state_closure, 2.0),
    ("tool_safe_full_trace", tool_safe_full_trace, 2.0),
]
