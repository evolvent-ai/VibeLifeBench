"""Trusted, fail-closed snapshots for the home studio simulation."""
from __future__ import annotations
import json, os
from datetime import datetime
from pathlib import Path
from typing import Any

SCENARIO_CLOCK_PATH = Path(os.environ.get("WORLD_CLOCK_FILE", "/world-clock/current.json"))
SCENARIO_CLOCK_REQUIRED = os.environ.get("SCENARIO_CLOCK_REQUIRED", "0") == "1"
USER_ID = "user_lwq"
CALENDAR_ID = "cal_lwq"

def scenario_clock() -> dict[str, Any]:
    try:
        payload = json.loads(SCENARIO_CLOCK_PATH.read_text(encoding="utf-8"))
        if not isinstance(payload, dict) or set(payload) != {"world_now"}:
            raise ValueError("invalid world clock payload")
        now = str(payload["world_now"]); datetime.fromisoformat(now.replace("Z", "+00:00"))
        return {"schema_version": 1, "now": now}
    except Exception as exc:
        raise RuntimeError(f"required world clock unavailable: {exc}") from exc

def _decode(value: Any) -> Any:
    if isinstance(value, str):
        try: return json.loads(value)
        except json.JSONDecodeError: return value
    return value

def _unwrap_envelope(value: Any, fetch_page=None) -> Any:
    if not isinstance(value, dict): return value
    rows = value.get("items")
    if not isinstance(rows, list) or ("total" not in value and "has_more" not in value): return value
    merged = list(rows); total = value.get("total"); page = int(value.get("page") or 1)
    while fetch_page is not None and value.get("has_more") and (not isinstance(total, int) or len(merged) < total):
        page += 1; nxt = fetch_page(page)
        if not isinstance(nxt, dict) or not isinstance(nxt.get("items"), list) or not nxt["items"]:
            value["_pagination_incomplete"] = True; break
        merged.extend(nxt["items"]); value = nxt
    return merged

def _call(env: Any, server: str, tool: str, **kwargs: Any) -> Any:
    cap = getattr(env, f"{server}_mock", None)
    if cap is None: return {"error": f"missing capability: {server}"}
    try:
        raw = _decode(cap.call_tool(tool, **kwargs))
        return _unwrap_envelope(raw, lambda p: _decode(cap.call_tool(tool, **{**kwargs, "page": p})))
    except BaseException as exc: return {"error": f"{type(exc).__name__}: {exc}"}

def _paged_call(env: Any, server: str, tool: str, rows_key: str, id_keys: tuple[str, ...], **kwargs: Any) -> Any:
    first = _call(env, server, tool, page=1, page_size=200, **kwargs)
    if not isinstance(first, dict) or not isinstance(first.get(rows_key), list): return first
    rows = list(first[rows_key]); total = first.get("total_results", first.get("total")); page = 2
    seen = {str(next((r.get(k) for k in id_keys if isinstance(r, dict) and r.get(k) is not None), "")) for r in rows}
    while isinstance(total, (int, float)) and len(rows) < int(total) and page < 100:
        nxt = _call(env, server, tool, page=page, page_size=max(len(rows), 1), **kwargs)
        if not isinstance(nxt, dict) or not isinstance(nxt.get(rows_key), list): first["_pagination_incomplete"] = True; break
        fresh = [r for r in nxt[rows_key] if str(next((r.get(k) for k in id_keys if isinstance(r, dict) and r.get(k) is not None), "")) not in seen]
        if not fresh: first["_pagination_incomplete"] = True; break
        rows.extend(fresh); seen.update(str(next((r.get(k) for k in id_keys if isinstance(r, dict) and r.get(k) is not None), "")) for r in fresh); page += 1
    first[rows_key] = rows; first["captured_count"] = len(rows); first["captured_complete"] = not isinstance(total, (int, float)) or len(rows) >= int(total); return first

def _workspace_snapshot(env: Any) -> dict[str, str]:
    fs = getattr(getattr(env, "workspace", None), "fs", None)
    if fs is None: return {}
    out = {}
    for name in ("studio_plan.md", "privacy_register.md", "purchase_ledger.md", "installation_log.md", "final_readiness.md"):
        path = f"/workspace/{name}"
        try:
            if fs.exists(path): out[path] = fs.read_file(path).decode("utf-8", errors="replace")[:200000]
        except Exception: pass
    return out

def capture_stage_snapshot(env: Any, stage_idx: int) -> dict[str, Any]:
    return {"stage": stage_idx, "scenario_clock": scenario_clock(), "workspace": _workspace_snapshot(env),
      "calendar": {"events": _call(env, "calendar", "list_events", calendar_id=CALENDAR_ID, max_results=500)},
      "email": {"inbox": _paged_call(env, "email", "get_emails", "emails", ("email_id", "id"), folder="INBOX"), "sent": _paged_call(env, "email", "get_emails", "emails", ("email_id", "id"), folder="Sent"), "drafts": _paged_call(env, "email", "get_drafts", "drafts", ("draft_id", "id"))},
      "content_platform": {"collections": _call(env, "content_platform", "list_collections", user_id=USER_ID), "notes": _call(env, "content_platform", "search_notes", query="", user_id=USER_ID)},
      "delivery_logistics": {"shipments": _call(env, "delivery_logistics", "list_shipments", user_id=USER_ID), "subscriptions": _call(env, "delivery_logistics", "list_subscriptions", user_id=USER_ID)},
      "ecommerce": {"orders": _call(env, "ecommerce", "list_orders", user_id=USER_ID, limit=100), "products": _call(env, "ecommerce", "list_products", query="")},
      "legal_search": {"saved": _call(env, "legal_search", "list_saved", user_id=USER_ID)},
      "notification_hub": {"notifications": _call(env, "notification_hub", "list_notifications", user_id=USER_ID, limit=500), "subscriptions": _call(env, "notification_hub", "list_subscriptions", user_id=USER_ID)},
      "notion": {"pages": _call(env, "notion", "API-post-search", query="", page_size=100)},
      "review_platform": {"merchants": _call(env, "review_platform", "list_merchants", query="Shanghai"), "reviews": _call(env, "review_platform", "list_reviews", merchant_id="merchant_0001")}}
