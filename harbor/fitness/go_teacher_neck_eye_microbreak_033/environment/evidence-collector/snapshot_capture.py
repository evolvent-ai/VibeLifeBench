"""Freeze the five service world at each visible stage boundary."""
from __future__ import annotations
import json
from typing import Any
from world_clock import read_clock

USER_ID = "user_liang_weimin"
CALENDAR_ID = "cal_go_teacher_primary"
WORKSPACE_FILES = ("stage_progress.md", "service_consistency_matrix.md", "risk_log.md", "calendar_change_log.md", "auth_log.md", "schedule_context_log.md", "equipment_budget.md", "notification_monitor_log.md", "final_review.md")

def _unwrap_envelope(value: Any, fetch_page=None) -> Any:
    if not isinstance(value, dict): return value
    rows = value.get("items")
    if not isinstance(rows, list) or ("total" not in value and "has_more" not in value): return value
    merged = list(rows)
    if fetch_page is not None and value.get("has_more"):
        page = int(value.get("page") or 1)
        total = int(value["total"]) if isinstance(value.get("total"), (int, float)) else None
        size = int(value.get("page_size") or 0) or max(len(merged), 1)
        while value.get("has_more") and page < ((total + size - 1) // size + 1 if total else 100):
            page += 1; nxt = fetch_page(page)
            if not isinstance(nxt, dict) or not isinstance(nxt.get("items"), list) or not nxt["items"]: break
            merged.extend(nxt["items"]); value = nxt
        if total is not None and len(merged) < total:
            return {"items": merged, "_pagination_incomplete": True, "_captured": len(merged), "_total": total}
    return merged

def _decode(value: Any) -> Any:
    if isinstance(value, str):
        try: return json.loads(value)
        except json.JSONDecodeError: return value
    return value

def _call(env: Any, server: str, tool: str, **kwargs: Any) -> Any:
    cap = getattr(env, server + "_mock", None)
    if cap is None: raise RuntimeError(f"missing capability: {server}")
    value = _decode(cap.call_tool(tool, **kwargs))
    return _unwrap_envelope(value, lambda page: _decode(cap.call_tool(tool, **{**kwargs, "page": page})))

def _workspace(env: Any) -> dict[str, str]:
    out = {}; fs = getattr(getattr(env, "workspace", None), "fs", None)
    if fs is None: return out
    for name in WORKSPACE_FILES:
        try:
            raw = fs.read_file("/workspace/" + name)
            out[name] = raw.decode("utf-8", "replace") if isinstance(raw, bytes) else str(raw)
        except Exception: pass
    return out

def capture_stage_snapshot(env: Any, stage_idx: int, expected_step: str) -> dict[str, Any]:
    read_clock(expected_step)
    result = {
        "stage": stage_idx,
        "calendar": {"list_events": _call(env, "calendar", "list_events", calendar_id=CALENDAR_ID, max_results=500)},
        "health_tracker": {"get_metrics": {k: _call(env, "health_tracker", "get_metrics", user_id=USER_ID, type=k, since="2026-07-01", until="2026-07-28", limit=1000) for k in ("steps", "sleep_minutes", "score")}, "list_workouts": _call(env, "health_tracker", "list_workouts", user_id=USER_ID, since="2026-07-01", until="2026-07-28", limit=500)},
        "email": {"inbox": _call(env, "email", "get_emails", folder="INBOX", page=1, page_size=50), "sent": _call(env, "email", "get_emails", folder="Sent", page=1, page_size=50), "drafts": _call(env, "email", "get_drafts", page=1, page_size=50)},
        "notification_hub": {"list_notifications": _call(env, "notification_hub", "list_notifications", user_id=USER_ID, unread_only=False, since="2026-07-01", limit=500), "list_subscriptions": _call(env, "notification_hub", "list_subscriptions", user_id=USER_ID)},
        "notion": {"API-post-search": _call(env, "notion", "API-post-search", query="Go instructor", filter={"value": "page"}, page_size=100)},
        "workspace": _workspace(env),
    }
    read_clock(expected_step)
    return result
