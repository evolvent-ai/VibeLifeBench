"""Freeze the graduate-exam preparation world at every stage boundary."""
from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

WORLD_CLOCK_FILE = Path(os.environ.get("WORLD_CLOCK_FILE", "/world-clock/current.json"))
USER_ID = "user_zhang"
CALENDAR_ID = "cal_zhang_main"
# AGENTS.md makes HEARTBEAT.md an agent-maintained journal and several rubrics
# score its content (subscription watch, quiet boundary, final closure), so it
# must be frozen with the workspace instead of treated as baseline scaffolding.
BASELINE_WORKSPACE_NAMES = {
    "AGENTS.md", "ARTIFACT_CONTRACT.md", "IDENTITY.md", "PERSONA.md",
    "SOUL.md", "TOOLS.md", "USER.md", "BUDGET.md", "HEALTH.md",
    "DOCUMENTS.md",
}
ALLOWED_WORKSPACE_SUFFIXES = (".md", ".txt", ".json", ".csv")


def scenario_clock() -> dict[str, Any]:
    try:
        payload = json.loads(WORLD_CLOCK_FILE.read_text(encoding="utf-8"))
        if not isinstance(payload, dict) or set(payload) != {"world_now"}:
            raise ValueError("world clock keys must be exactly {world_now}")
        value = payload.get("world_now")
        if not isinstance(value, str) or not value:
            raise ValueError("world_now must be a non-empty timestamp")
        from datetime import datetime
        if datetime.fromisoformat(value.replace("Z", "+00:00")).tzinfo is None:
            raise ValueError("world_now must include a timezone")
        return {"schema_version": 1, "now": value}
    except Exception as exc:
        raise RuntimeError(
            f"required world clock unavailable at {WORLD_CLOCK_FILE}: {exc}"
        ) from exc


def _decode(value: Any) -> Any:
    if isinstance(value, str):
        try:
            return json.loads(value)
        except json.JSONDecodeError:
            return value
    return value


def _unwrap_envelope(value: Any, fetch_page=None) -> Any:
    if not isinstance(value, dict):
        return value
    rows = value.get("items")
    if not isinstance(rows, list):
        return value
    if "total" not in value and "has_more" not in value:
        return value
    merged = list(rows)
    if fetch_page is not None and value.get("has_more"):
        page = int(value.get("page") or 1)
        total = int(value["total"]) if isinstance(value.get("total"), (int, float)) else None
        size = int(value.get("page_size") or 0) or max(len(merged), 1)
        max_pages = ((total + size - 1) // size + 1) if total is not None else 1000
        seen = {json.dumps(row, sort_keys=True, default=str) for row in merged}
        while value.get("has_more") and page < max_pages:
            page += 1
            nxt = fetch_page(page)
            if not isinstance(nxt, dict):
                break
            fresh = []
            for row in nxt.get("items") or []:
                key = json.dumps(row, sort_keys=True, default=str)
                if key not in seen:
                    fresh.append(row)
                    seen.add(key)
            if not fresh:
                break
            merged.extend(fresh)
            value = nxt
        if total is not None and len(merged) < total:
            return {
                "items": merged,
                "_pagination_incomplete": True,
                "_captured": len(merged),
                "_total": total,
            }
    return merged


def _call(env: Any, server: str, tool: str, **kwargs: Any) -> Any:
    cap = getattr(env, f"{server}_mock", None)
    if cap is None:
        return {"error": f"missing capability: {server}"}
    try:
        value = _decode(cap.call_tool(tool, **kwargs))
        return _unwrap_envelope(
            value,
            lambda page: _decode(cap.call_tool(tool, **{**kwargs, "page": page})),
        )
    except BaseException as exc:
        return {"error": f"{type(exc).__name__}: {exc}"}


def _paged_call(
    env: Any,
    server: str,
    tool: str,
    *,
    rows_key: str,
    id_keys: tuple[str, ...],
    **kwargs: Any,
) -> Any:
    first = _call(env, server, tool, page=1, page_size=200, **kwargs)
    if not isinstance(first, dict):
        return first

    def row_id(row: Any) -> str:
        if not isinstance(row, dict):
            return ""
        return str(next((row.get(key) for key in id_keys if row.get(key) is not None), ""))

    merged = [row for row in (first.get(rows_key) or []) if isinstance(row, dict)]
    applied = int(first.get("page_size") or 0) or max(len(merged), 1)
    raw_total = first.get("total_results", first.get("total"))
    total = int(raw_total) if isinstance(raw_total, (int, float)) else None
    seen = {row_id(row) for row in merged}
    page = 2
    max_pages = ((total + applied - 1) // applied + 1) if total is not None else 1
    while total is not None and len(merged) < total and page <= max_pages:
        nxt = _call(env, server, tool, page=page, page_size=applied, **kwargs)
        if not isinstance(nxt, dict):
            break
        fresh = [
            row for row in (nxt.get(rows_key) or [])
            if isinstance(row, dict) and row_id(row) not in seen
        ]
        if not fresh:
            break
        merged.extend(fresh)
        seen.update(row_id(row) for row in fresh)
        page += 1
    first[rows_key] = merged
    first["captured_count"] = len(merged)
    if total is not None:
        first["captured_complete"] = len(merged) >= total
    return first


def _email_snapshot(env: Any, folder: str) -> dict[str, Any]:
    """Freeze one mailbox folder from its listing alone.

    The listing carries subject/addresses/date per message, which is everything
    the evidence readers consume.  A per-message ``read_email`` walk adds
    hundreds of MCP round trips per stage — the difference between fitting in
    the collect hook's fixed budget and timing out before the stage evidence is
    published — and marks every seeded message read, so ``details`` stays an
    explicitly empty list rather than an expensive, unused field.
    """
    listing = _paged_call(
        env, "email", "get_emails", rows_key="emails",
        id_keys=("email_id", "id"), folder=folder,
    )
    return {"listing": listing, "details": []}


def _workspace_snapshot(env: Any) -> dict[str, str]:
    fs = getattr(getattr(env, "workspace", None), "fs", None)
    if fs is None:
        return {}
    out: dict[str, str] = {}
    seen: set[str] = set()

    def visit(path: str, depth: int) -> None:
        if path in seen or depth < 0 or len(out) >= 200:
            return
        seen.add(path)
        try:
            children = fs.list_dir(path)
        except Exception:
            return
        for child in children:
            full = f"{path.rstrip('/')}/{child}"
            if child in BASELINE_WORKSPACE_NAMES or child.startswith("."):
                continue
            if child.lower().endswith(ALLOWED_WORKSPACE_SUFFIXES):
                try:
                    raw = fs.read_file(full)
                    text = raw.decode("utf-8", "replace") if isinstance(raw, bytes) else str(raw)
                    if text.strip():
                        out[full] = text[:200000]
                except Exception:
                    pass
            elif depth:
                visit(full, depth - 1)

    visit("/workspace", 4)
    return out


def _notion_snapshot(env: Any) -> dict[str, Any]:
    pages = _call(
        env, "notion", "API-post-search", query="",
        filter={"value": "page", "property": "object"}, page_size=100,
    )
    databases = _call(
        env, "notion", "API-post-search", query="",
        filter={"value": "database", "property": "object"}, page_size=100,
    )

    def ids(data: Any) -> list[str]:
        if not isinstance(data, dict):
            return []
        return [
            str(row["id"]) for row in data.get("results") or []
            if isinstance(row, dict) and row.get("id")
        ]

    page_blocks = {
        page_id: _call(env, "notion", "API-get-block-children", block_id=page_id, page_size=100)
        for page_id in ids(pages)
    }
    database_rows: dict[str, Any] = {}
    for database_id in ids(databases):
        database_rows[database_id] = _call(
            env, "notion", "API-post-database-query",
            database_id=database_id, page_size=100,
        )
    # Per-row ``API-get-block-children`` would cost one MCP round trip for every
    # database row (200+ rows are seeded).  Evidence readers resolve block
    # children for pages only — ``page_blocks`` already covers every search
    # result — so ``row_children`` is kept as a key but not walked.
    return {
        "pages": pages,
        "databases": databases,
        "page_blocks": page_blocks,
        "database_rows": database_rows,
        "row_children": {},
    }


def capture_stage_snapshot(env: Any, stage_idx: int) -> dict[str, Any]:
    orders = _call(env, "ecommerce", "list_orders", user_id=USER_ID, limit=500)
    order_rows = orders if isinstance(orders, list) else (
        orders.get("orders", orders.get("items", [])) if isinstance(orders, dict) else []
    )
    order_details = {}
    order_tracking = {}
    for row in order_rows:
        order_id = (row.get("order_id") or row.get("id")) if isinstance(row, dict) else None
        if order_id:
            order_details[str(order_id)] = _call(env, "ecommerce", "get_order", order_id=order_id)
            order_tracking[str(order_id)] = _call(env, "ecommerce", "track_order", order_id=order_id)

    return {
        "stage": stage_idx,
        "scenario_clock": scenario_clock(),
        "calendar": {
            "events": _call(env, "calendar", "list_events", max_results=1000),
            "calendars": _call(env, "calendar", "list_calendars"),
        },
        "banking": {
            "accounts": _call(env, "banking", "list_accounts", user_id=USER_ID),
            "transactions": {
                account_id: _call(env, "banking", "list_transactions", account_id=account_id, limit=500)
                for account_id in ("acct_zhang_budget",)
            },
            "payees": _call(env, "banking", "list_payees", user_id=USER_ID),
            "pending_payments": _call(env, "banking", "list_pending_payments", user_id=USER_ID, limit=500),
            "recurring": _call(env, "banking", "list_recurring", user_id=USER_ID),
        },
        "health_tracker": {
            "metrics": {
                metric: _call(
                    env, "health_tracker", "get_metrics",
                    user_id="mother_li", type=metric, limit=1000,
                )
                for metric in ("steps", "sleep_minutes", "heart_rate", "blood_pressure", "pain")
            },
            "workouts": _call(env, "health_tracker", "list_workouts", user_id="mother_li", limit=1000),
            "goals": _call(env, "health_tracker", "get_goals", user_id="mother_li"),
            "alerts": _call(env, "health_tracker", "list_health_alerts", user_id="mother_li"),
        },
        "ecommerce": {
            "products": _call(env, "ecommerce", "search_products", query="", limit=1000),
            "cart": _call(env, "ecommerce", "get_cart", user_id=USER_ID),
            "addresses": _call(env, "ecommerce", "list_addresses", user_id=USER_ID),
            "orders": orders,
            "order_details": order_details,
            "order_tracking": order_tracking,
        },
        "notification_hub": {
            "subscriptions": _call(env, "notification_hub", "list_subscriptions", user_id=USER_ID),
            "notifications": _call(env, "notification_hub", "list_notifications", user_id=USER_ID, limit=500),
        },
        "email": {
            "inbox": _email_snapshot(env, "INBOX"),
            "sent": _email_snapshot(env, "Sent"),
            "drafts": _paged_call(
                env, "email", "get_drafts", rows_key="drafts", id_keys=("draft_id", "id"),
            ),
        },
        "notion": _notion_snapshot(env),
        "workspace": _workspace_snapshot(env),
    }
