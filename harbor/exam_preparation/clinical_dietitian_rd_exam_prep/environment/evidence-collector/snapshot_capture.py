"""Freeze the five service world at each visible stage boundary."""
from __future__ import annotations
import json
from typing import Any
from world_clock import read_clock

USER_ID = "user_chen"
CALENDAR_ID = "cal_main"
WORKSPACE_FILES = ("stage_progress.md", "official_evidence_log.md", "internship_tracker.md", "risk_log.md", "mock_score_log.md", "auth_log.md", "final_review.md")

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

def _page_blocks(env: Any, search: Any) -> dict[str, Any]:
    """Freeze every page's block children next to the search results.

    The rubric projector answers notion API-get-block-children from this
    mapping (tests/rubrics/_helpers.py), so a snapshot without it makes every
    child-block read look empty and misjudges agents that write page content
    into blocks instead of page properties.
    """
    out: dict[str, Any] = {}
    if not isinstance(search, dict): return out
    rows = search.get("results") if isinstance(search.get("results"), list) else None
    if rows is None: rows = search.get("items") if isinstance(search.get("items"), list) else []
    for row in rows:
        if not isinstance(row, dict): continue
        page_id = row.get("id") or row.get("page_id")
        if not page_id or str(page_id) in out: continue
        merged: list[Any] = []
        cursor: Any = None
        for _ in range(100):
            kwargs: dict[str, Any] = {"block_id": str(page_id), "page_size": 10000}
            if cursor is not None: kwargs["start_cursor"] = cursor
            try:
                value = _decode(getattr(env, "notion_mock").call_tool("API-get-block-children", **kwargs))
            except Exception:
                merged = []; break
            if isinstance(value, dict) and isinstance(value.get("results"), list):
                merged.extend(value["results"])
                if value.get("has_more") and value.get("next_cursor"):
                    cursor = value["next_cursor"]; continue
            break
        out[str(page_id)] = {"results": merged}
    return out

def _email_details(env: Any, inbox: Any, sent: Any) -> dict[str, Any]:
    """Freeze read_email detail for the messages the rubrics match terms in.

    Folder listings are metadata-only by SPEC (bodies are served exclusively
    by read_email), so a snapshot carrying only listings makes every frozen
    read_email projection bodyless and every body-term check unsatisfiable.
    Detail reads are bounded: all listed sent mail plus inbox mail already
    marked read — exactly the rows the frozen read_email projection can be
    asked to serve.
    """
    out: dict[str, Any] = {}
    email_ids: list[Any] = []
    for listing, only_read in ((sent, False), (inbox, True)):
        rows = listing.get("emails") if isinstance(listing, dict) else None
        if not isinstance(rows, list): continue
        for row in rows:
            if not isinstance(row, dict): continue
            if only_read and row.get("is_read") is not True: continue
            email_id = row.get("email_id") or row.get("id")
            if email_id and str(email_id) not in out:
                email_ids.append(email_id)
                out[str(email_id)] = None
    cap = getattr(env, "email_mock", None)
    if cap is None: return {}
    for email_id in email_ids:
        try:
            detail = _call(env, "email", "read_email", email_id=str(email_id))
        except Exception:
            out.pop(str(email_id), None)
            continue
        if isinstance(detail, dict) and not detail.get("error"):
            out[str(email_id)] = detail
        else:
            out.pop(str(email_id), None)
    return out

def capture_stage_snapshot(env: Any, stage_idx: int, expected_step: str) -> dict[str, Any]:
    read_clock(expected_step)
    inbox = _call(env, "email", "get_emails", folder="INBOX", page=1, page_size=50)
    sent = _call(env, "email", "get_emails", folder="Sent", page=1, page_size=50)
    drafts = _call(env, "email", "get_drafts", page=1, page_size=50)
    result = {
        "stage": stage_idx,
        "calendar": {"list_events": _call(env, "calendar", "list_events", calendar_id=CALENDAR_ID, max_results=500)},
        "health_tracker": {"get_metrics": {k: _call(env, "health_tracker", "get_metrics", user_id=USER_ID, type=k, since="2026-08-01", until="2026-11-30", limit=1000) for k in ("steps", "sleep_minutes", "heart_rate", "score")}, "list_health_alerts": _call(env, "health_tracker", "list_health_alerts", user_id=USER_ID, limit=100)},
        "email": {"inbox": inbox, "sent": sent, "drafts": drafts, "details": _email_details(env, inbox, sent)},
        "notification_hub": {
            "list_notifications": _call(env, "notification_hub", "list_notifications", user_id=USER_ID, unread_only=False, since="2026-08-01", limit=500),
            "list_subscriptions": _call(env, "notification_hub", "list_subscriptions", user_id=USER_ID),
            "get_account_feed": _call(env, "notification_hub", "get_account_feed", account_id="cdr_exam_updates", limit=200),
        },
        "notion": {"API-post-search": _call(env, "notion", "API-post-search", query="", filter={"value": "page"}, page_size=100)},
        "workspace": _workspace(env),
    }
    result["notion"]["page_blocks"] = _page_blocks(env, result["notion"]["API-post-search"])
    read_clock(expected_step)
    return result
