from __future__ import annotations

import json
import re
from datetime import datetime
from harbor_evidence import response as evidence_response
from harbor_evidence import snapshot as evidence_snapshot
from harbor_evidence import trace as evidence_trace


STAGE_COUNT = 25
WORKSPACE_DIRS = [
    "/terrarium/openclaw/workspace/workspace",
    "/terrarium/openclaw/workspace",
    "/workspace",
]


def _as_text(value) -> str:
    if value is None:
        return ""
    if isinstance(value, bytes):
        return value.decode("utf-8", errors="ignore")
    return str(value)


def _read(env, path: str) -> str:
    stage = int(getattr(env, "current_stage", STAGE_COUNT - 1))
    data = evidence_snapshot(env, stage)
    workspace = data.get("workspace", {})
    if not isinstance(workspace, dict):
        raise RuntimeError(f"frozen workspace evidence for stage {stage} is not an object")
    basename = path.rstrip("/").rsplit("/", 1)[-1]
    for recorded, content in workspace.items():
        if str(recorded).rstrip("/").rsplit("/", 1)[-1] == basename:
            return _as_text(content)
    return ""


def wfile(env, basename: str) -> str:
    base = basename.split("/")[-1]
    for root in WORKSPACE_DIRS:
        text = _read(env, f"{root}/{base}")
        if text:
            return text
    return ""


def _agent_reply(env, stage_idx: int) -> str:
    return evidence_response(env, stage_idx)


def _trace_calls(env, start: int = 0, end: int = 24) -> list[dict]:
    calls = []
    for idx in range(start, end + 1):
        data = evidence_trace(env, idx)
        if isinstance(data, list):
            calls.extend(x for x in data if isinstance(x, dict))
    return calls


def _trace_text(env, start: int = 0, end: int = 24) -> str:
    return json.dumps(_trace_calls(env, start, end), ensure_ascii=False).lower()


def _call_name(call: dict) -> str:
    name = call.get("function_name") or call.get("name") or call.get("function")
    if isinstance(name, dict):
        name = name.get("name")
    return _as_text(name).strip().lower()


_TRACE_SERVICES = {
    "calendar", "notion", "ecommerce", "banking", "email", "notification_hub", "health_tracker"
}
_TRACE_TOOLS = {
    "list_events", "get_event", "create_event", "update_event", "delete_event", "search_events",
    "api-retrieve-a-page", "api-post-search", "api-post-database-query", "api-get-block-children", "api-patch-block-children",
    "get_product", "search_products", "add_to_cart", "place_order", "list_orders", "get_order", "track_order",
    "list_accounts", "list_transactions", "get_account", "transfer", "pay_payee",
    "search_emails", "get_emails", "read_email", "send_email", "reply_email", "get_drafts",
    "create_subscription", "list_subscriptions", "pause_subscription", "update_subscription", "delete_subscription",
    "get_metrics", "list_health_alerts",
}


def _successful_trace_calls(env, start: int = 0, end: int = 24) -> list[dict]:
    """Return only calls paired with an explicit successful tool result."""
    return [call for call in _trace_calls(env, start, end) if call.get("success") is True]


def _stage_text(env, idx: int) -> str:
    return "\n".join([_agent_reply(env, idx), wfile(env, "CONTROL_CENTER.md"), wfile(env, "BUDGET_LEDGER.md"), wfile(env, "HEALTH_LOG.md")])


def _workspace_text(env) -> str:
    files = [
        "CONTROL_CENTER.md",
        "BUDGET_LEDGER.md",
        "HEALTH_LOG.md",
        "HEARTBEAT.md",
    ]
    return "\n".join(wfile(env, x) for x in files)


def _all_corpus(env) -> str:
    parts = [_workspace_text(env)]
    for i in range(STAGE_COUNT):
        parts.append(_agent_reply(env, i))
    return "\n".join(parts)


def has(text: str, *words: str) -> bool:
    low = text.lower()
    return all(w.lower() in low for w in words)


def any_has(text: str, words: list[str]) -> bool:
    low = text.lower()
    return any(w.lower() in low for w in words)


def count_hits(text: str, groups: list[list[str]]) -> int:
    return sum(1 for g in groups if any_has(text, g))


def _tool_used(env, words: list[str], start: int = 0, end: int = 24) -> bool:
    names = "\n".join(_call_name(call) for call in _successful_trace_calls(env, start, end))
    return any_has(names, words)


def _stage_trace_has(env, stage: int, groups: list[list[str]]) -> bool:
    return _stage_trace_all(env, stage, groups)


def _stage_trace_all(env, stage: int, groups: list[list[str]]) -> bool:
    calls = _successful_trace_calls(env, stage, stage)
    for group in groups:
        matched = False
        for token in group:
            needle = str(token).strip().lower()
            for call in calls:
                name = _call_name(call)
                if needle in _TRACE_SERVICES:
                    matched = name.startswith(needle + "__")
                elif needle in _TRACE_TOOLS:
                    matched = name.endswith("__" + needle) or name == needle
                else:
                    matched = needle in name
                if matched:
                    break
            if matched:
                break
        if not matched:
            return False
    return True


def _trace_count(env, stage: int, words: list[str]) -> int:
    return sum(
        1
        for call in _successful_trace_calls(env, stage, stage)
        if any(str(word).lower() in _call_name(call) for word in words)
    )


def _stage_reply_has(env, stage: int, groups: list[list[str]]) -> bool:
    return count_hits(_agent_reply(env, stage), groups) == len(groups)


def _workspace_has(env, groups: list[list[str]]) -> bool:
    return count_hits(_workspace_text(env), groups) == len(groups)


def _workspace_file_has(env, basename: str, groups: list[list[str]]) -> bool:
    return count_hits(wfile(env, basename), groups) == len(groups)


def _subscription_sources_active(env, required: list[tuple[str, str]]) -> bool:
    rows = _notifications(env)
    return all(
        any(
            str(row.get("source") or "") == source
            and str(row.get("target") or "") == target
            and str(row.get("status") or "").lower() == "active"
            for row in rows
        )
        for source, target in required
    )


def _trace_result_has(env, stage: int, predicate) -> bool:
    return any(predicate(call.get("result")) for call in _successful_trace_calls(env, stage, stage))


def _trace_purchase_contains(env, tokens: list[str], start: int = 0, end: int = 24) -> bool:
    """Inspect only mutating cart/order calls when enforcing purchase policy."""
    purchase_tools = {"ecommerce__add_to_cart", "ecommerce__place_order", "add_to_cart", "place_order"}
    wanted = [token.lower() for token in tokens]
    for call in _successful_trace_calls(env, start, end):
        if _call_name(call) not in purchase_tools:
            continue
        payload = json.dumps(call.get("arguments") or {}, ensure_ascii=False).lower()
        if any(token in payload for token in wanted):
            return True
    return False


def _late_trace_services(env, start: int, end: int, services: list[str], minimum: int) -> bool:
    names = {_call_name(call).split("__", 1)[0] for call in _successful_trace_calls(env, start, end)}
    return sum(service in names for service in services) >= minimum


def _call_tool(env, server: str, tool: str, **kwargs):
    stage = int(getattr(env, "current_stage", STAGE_COUNT - 1))
    state = evidence_snapshot(env, stage)
    section = state.get(server, {})
    if not isinstance(section, dict):
        raise RuntimeError(f"frozen {server} evidence is not an object")
    if server == "calendar" and tool == "list_events":
        return section.get("events", section.get("calendar", {}).get("events", []))
    if server == "banking" and tool == "list_accounts":
        return section.get("accounts", [])
    if server == "banking" and tool == "list_transactions":
        txs = section.get("transactions", {})
        if isinstance(txs, dict):
            return txs.get(kwargs.get("account_id"), next(iter(txs.values()), []))
        return txs
    if server == "ecommerce" and tool == "list_orders":
        return section.get("orders", [])
    if server == "ecommerce" and tool == "get_order":
        details = section.get("order_details", {})
        oid = str(kwargs.get("order_id") or "")
        if isinstance(details, dict):
            return details.get(oid, {})
        return next((row for row in details if isinstance(row, dict) and str(row.get("order_id") or row.get("id") or "") == oid), {})
    if server == "email":
        if tool in {"search_emails", "get_emails"}:
            folder = str(kwargs.get("folder") or "INBOX").lower()
            box = section.get("sent" if folder == "sent" else "inbox", {})
            return box.get("listing", box) if isinstance(box, dict) else box
        if tool == "get_drafts":
            return section.get("drafts", [])
        if tool == "read_email":
            eid = str(kwargs.get("email_id") or kwargs.get("id") or "")
            for box_name in ("inbox", "sent"):
                box = section.get(box_name, {})
                for row in (box.get("details", []) if isinstance(box, dict) else []):
                    if isinstance(row, dict) and str(row.get("email_id") or row.get("id") or "") == eid:
                        return row
            return {}
    if server == "notification_hub":
        if tool == "list_subscriptions":
            return section.get("subscriptions", [])
        if tool == "list_notifications":
            return section.get("notifications", [])
    if server == "health_tracker":
        if tool == "get_metrics":
            metrics = section.get("metrics", {})
            return metrics.get(kwargs.get("type"), []) if isinstance(metrics, dict) else metrics
        if tool == "list_health_alerts":
            return section.get("alerts", [])
    if server == "notion":
        if tool == "API-post-search":
            key = "databases" if (kwargs.get("filter") or {}).get("value") == "database" else "pages"
            return section.get(key, {})
        if tool == "API-get-block-children":
            block_id = str(kwargs.get("block_id") or "")
            return (section.get("page_blocks", {}).get(block_id)
                    or section.get("row_children", {}).get(block_id)
                    or {})
        if tool == "API-post-database-query":
            return section.get("database_rows", {}).get(str(kwargs.get("database_id") or ""), {})
    raise RuntimeError(f"unsupported frozen evidence lookup: {server}.{tool}")


def _orders(env) -> list[dict]:
    data = _call_tool(env, "ecommerce", "list_orders", user_id="user_zhang", limit=100)
    if isinstance(data, dict):
        data = data.get("orders") or data.get("items") or []
    return data if isinstance(data, list) else []


def _orders_text(env) -> str:
    return json.dumps(_orders(env), ensure_ascii=False)


def _order_detail_text(env) -> str:
    parts = [_orders_text(env)]
    for order in _orders(env):
        oid = order.get("order_id") or order.get("id")
        if not oid:
            continue
        detail = _call_tool(env, "ecommerce", "get_order", order_id=oid)
        if detail is not None:
            parts.append(json.dumps(detail, ensure_ascii=False))
    return "\n".join(parts)


def _paid_order_has(env, groups: list[list[str]]) -> bool:
    text = _order_detail_text(env)
    return any_has(text, ["paid", "paid", "order_id"]) and count_hits(text, groups) == len(groups)


def _emails_text(env) -> str:
    data = _call_tool(env, "email", "search_emails", query="", folder="INBOX", page=1, page_size=100)
    if isinstance(data, dict):
        data = data.get("emails") or data.get("messages") or data.get("items") or []
    return json.dumps(data, ensure_ascii=False) if data is not None else ""


def _notifications(env) -> list[dict]:
    data = _call_tool(env, "notification_hub", "list_subscriptions", user_id="user_zhang")
    if isinstance(data, dict):
        data = data.get("subscriptions") or data.get("items") or []
    return data if isinstance(data, list) else []


def _subscriptions_text(env) -> str:
    return json.dumps(_notifications(env), ensure_ascii=False)


def _calendar_events(env) -> list[dict]:
    data = _call_tool(env, "calendar", "list_events", calendar_id="cal_zhang_main", time_min="2026-11-18T00:00:00+08:00", time_max="2026-12-24T00:00:00+08:00")
    if isinstance(data, dict):
        data = data.get("events") or data.get("items") or []
    return data if isinstance(data, list) else []


def _health_text(env) -> str:
    parts = []
    for type_name in ["heart_rate", "steps"]:
        data = _call_tool(
            env,
            "health_tracker",
            "get_metrics",
            user_id="mother_li",
            type=type_name,
            since="2026-11-18",
            until="2026-12-23",
            limit=200,
        )
        if data is not None:
            parts.append(json.dumps(data, ensure_ascii=False))
    alerts = _call_tool(env, "health_tracker", "list_health_alerts", user_id="mother_li", limit=50)
    if alerts is not None:
        parts.append(json.dumps(alerts, ensure_ascii=False))
    return "\n".join(parts)


def _sent_or_draft_text(env) -> str:
    parts = []
    for tool, kwargs in [
        ("get_drafts", {"page": 1, "page_size": 100}),
        ("search_emails", {"query": "Dr. Wang", "folder": "Sent", "page": 1, "page_size": 100}),
    ]:
        data = _call_tool(env, "email", tool, **kwargs)
        if data is not None:
            parts.append(json.dumps(data, ensure_ascii=False))
    return "\n".join(parts)


def _hours(start: str, end: str) -> float:
    try:
        s = datetime.fromisoformat(start.replace("Z", "+00:00"))
        e = datetime.fromisoformat(end.replace("Z", "+00:00"))
        return (e - s).total_seconds() / 3600
    except Exception:
        return 0.0


def calendar_has_no_long_study_blocks(env) -> bool:
    events = _calendar_events(env)
    if not events:
        text = _all_corpus(env)
        return not any_has(text, ["5hourscontinuous study", "6hourscontinuous study", "5-hour continuous", "6-hour continuous"])
    for ev in events:
        text = " ".join(
            str(ev.get(key) or "")
            if not isinstance(ev.get(key), dict)
            else " ".join(str(value or "") for value in ev[key].values())
            for key in ("summary", "description")
        ).lower()
        if any(k in text for k in ["study", "mock", "incorrect", "problems", "math"]):
            start = ev.get("start_dt") or ev.get("start") or ""
            end = ev.get("end_dt") or ev.get("end") or ""
            if isinstance(start, dict):
                start = start.get("dateTime") or start.get("date") or ""
            if isinstance(end, dict):
                end = end.get("dateTime") or end.get("date") or ""
            if _hours(str(start), str(end)) > 4.01:
                return False
    return True


def _calendar_text(env) -> str:
    return json.dumps(_calendar_events(env), ensure_ascii=False)


def _calendar_has(env, groups: list[list[str]]) -> bool:
    return _calendar_event_count(env, groups) >= 1


def _calendar_event_count(env, groups: list[list[str]]) -> int:
    total = 0
    for ev in _calendar_events(env):
        text = json.dumps(ev, ensure_ascii=False)
        if count_hits(text, groups) == len(groups):
            total += 1
    return total


def _valid_full_length_mock_events(env, required: int = 4) -> bool:
    events = []
    dates = set()
    for event in _calendar_events(env):
        text = json.dumps(event, ensure_ascii=False).lower()
        if "full-length mock" not in text and "full length mock" not in text:
            continue
        start = event.get("start") or event.get("start_dt") or {}
        end = event.get("end") or event.get("end_dt") or {}
        if isinstance(start, dict):
            start = start.get("dateTime") or start.get("date") or ""
        if isinstance(end, dict):
            end = end.get("dateTime") or end.get("date") or ""
        if _hours(str(start), str(end)) <= 0:
            continue
        dates.add(str(start)[:10])
        events.append(event)
    return len(events) >= required and len(dates) >= required


def _notion_text(env) -> str:
    parts = []
    search = _call_tool(env, "notion", "API-post-search", query="", page_size=100)
    if search is not None:
        parts.append(json.dumps(search, ensure_ascii=False))
        results = search.get("results") if isinstance(search, dict) else []
        for page in results or []:
            if not isinstance(page, dict) or page.get("object") != "page":
                continue
            pid = page.get("id")
            if not pid:
                continue
            children = _call_tool(env, "notion", "API-get-block-children", block_id=pid, page_size=100)
            if children is not None:
                parts.append(json.dumps(children, ensure_ascii=False))
    for database_id in ["db_exam_progress", "db_budget", "db_health"]:
        data = _call_tool(env, "notion", "API-post-database-query", database_id=database_id, page_size=100)
        if data is not None:
            parts.append(json.dumps(data, ensure_ascii=False))
    children = _call_tool(env, "notion", "API-get-block-children", block_id="page_control_root", page_size=100)
    if children is not None:
        parts.append(json.dumps(children, ensure_ascii=False))
    return "\n".join(parts)


def _notion_has(env, groups: list[list[str]]) -> bool:
    return count_hits(_notion_text(env), groups) == len(groups)


def _transactions_text(env) -> str:
    parts = []
    accounts = _call_tool(env, "banking", "list_accounts", user_id="user_zhang")
    if accounts is not None:
        parts.append(json.dumps(accounts, ensure_ascii=False))
    txs = _call_tool(
        env,
        "banking",
        "list_transactions",
        account_id="acct_zhang_budget",
        since="2026-11-18",
        until="2026-12-24",
        limit=200,
    )
    if txs is not None:
        parts.append(json.dumps(txs, ensure_ascii=False))
    return "\n".join(parts)


def _transactions(env) -> list[dict]:
    data = _call_tool(
        env,
        "banking",
        "list_transactions",
        account_id="acct_zhang_budget",
        since="2026-11-18",
        until="2026-12-24",
        limit=500,
    )
    if isinstance(data, dict):
        data = data.get("items") or data.get("transactions") or []
    return [row for row in data if isinstance(row, dict)] if isinstance(data, list) else []


def _reconciled_order_groups(env, product_groups: list[list[str]]) -> bool:
    """Require each requested product group in a paid order with a matching bank debit."""
    transactions = _transactions(env)
    matched_products = set()
    for order in _orders(env):
        order_id = str(order.get("order_id") or order.get("id") or "")
        if not order_id:
            continue
        detail = _call_tool(env, "ecommerce", "get_order", order_id=order_id)
        if not isinstance(detail, dict) or str(detail.get("status") or "").lower() != "paid":
            continue
        total = detail.get("total_minor")
        if not isinstance(total, int) or total <= 0:
            continue
        bank_match = any(
            tx.get("amount_minor") == -total
            and order_id.lower() in str(tx.get("memo") or "").lower()
            for tx in transactions
        )
        if not bank_match:
            continue
        items = json.dumps(detail.get("items") or [], ensure_ascii=False).lower()
        for index, group in enumerate(product_groups):
            if any(str(token).lower() in items for token in group):
                matched_products.add(index)
    return len(matched_products) == len(product_groups)


def no_forbidden_server_trace(env) -> bool:
    t = _trace_text(env)
    return not any(k in t for k in ["flight_booking", "hotel_booking", "brokerage"])


def order_text(env) -> str:
    return json.dumps(_orders(env), ensure_ascii=False) + "\n" + _all_corpus(env)


__all__ = [name for name in globals() if not name.startswith("__") and name not in {"json", "re", "datetime"}]
