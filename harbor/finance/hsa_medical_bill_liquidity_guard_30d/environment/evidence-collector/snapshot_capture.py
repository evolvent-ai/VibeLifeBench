"""Task-local stage snapshots for the six financial MCP services."""
from __future__ import annotations
import json
import os
from pathlib import Path
from typing import Any

SCENARIO_CLOCK_PATH = Path(os.environ.get("WORLD_CLOCK_FILE", os.environ.get("SCENARIO_CLOCK_PATH", "/world-clock/current.json")))
SCENARIO_CLOCK_REQUIRED = os.environ.get("SCENARIO_CLOCK_REQUIRED", "0") == "1"
USER_ID = "usr_fin"

def scenario_clock() -> dict[str, Any]:
    try:
        payload = json.loads(SCENARIO_CLOCK_PATH.read_text(encoding="utf-8"))
        if set(payload) != {"world_now"} or not isinstance(payload.get("world_now"), str):
            raise ValueError("invalid scenario clock payload")
        return {"schema_version": 1, "world_now": payload["world_now"]}
    except Exception as exc:
        if SCENARIO_CLOCK_REQUIRED:
            raise RuntimeError(f"required scenario clock unavailable: {exc}") from exc
        return {"schema_version": 1, "step": "unknown", "now": ""}

def _decode(value: Any) -> Any:
    if isinstance(value, str):
        try:
            return json.loads(value)
        except json.JSONDecodeError:
            return value
    return value

def _unwrap_envelope(value, fetch_page=None):
    """Unwrap the paginated envelope back into a bare row list.

    The current mock servers return {items, total, page, page_size, has_more}
    where they used to return a plain JSON array. Every rubric key chain was
    written against the array: a missing key yields [] instead of raising, and
    the rubric only asks "is there a non-empty value" -- so the switch does not
    error, it only zeroes the evidence, and the symptom looks exactly like the
    agent failing the task. Unwrapping here keeps all downstream code unchanged.

    Shapes that are not envelopes pass through untouched: error sentinels, the
    email listings ({emails, total_results, ...}), and business objects that
    merely happen to carry an "items" field.

    Paging is not optional. max_results is a page size, not a data cap; when
    has_more is true there are rows outside the snapshot, and evidence that
    never enters the snapshot can never be scored.
    """
    if not isinstance(value, dict):
        return value
    rows = value.get("items")
    if not isinstance(rows, list):
        return value
    if "total" not in value and "has_more" not in value:
        return value          # business object with an "items" field, not an envelope

    merged = list(rows)
    if fetch_page is not None and value.get("has_more"):
        seen = {id(r) for r in merged}
        page = int(value.get("page") or 1)
        total = value.get("total")
        total = int(total) if isinstance(total, (int, float)) else None
        # Page ceiling: rows over page size, +1 to tolerate a total that grew
        # between two calls rather than stopping short.
        size = int(value.get("page_size") or 0) or max(len(merged), 1)
        max_pages = ((total + size - 1) // size + 1) if total else 1
        while value.get("has_more") and page < max_pages:
            page += 1
            nxt = fetch_page(page)
            if not isinstance(nxt, dict):
                break
            fresh = [r for r in (nxt.get("items") or []) if id(r) not in seen]
            if not fresh:
                break
            seen.update(id(r) for r in fresh)
            merged.extend(fresh)
            value = nxt
        if total is not None and len(merged) < total:
            # A short capture must stay detectable, never a silent prefix.
            return {"items": merged, "_pagination_incomplete": True,
                    "_captured": len(merged), "_total": total}
    return merged


def _call(env: Any, server: str, tool: str, **kwargs: Any) -> Any:
    cap = getattr(env, f"{server}_mock", None)
    if cap is None:
        return {"error": f"missing capability: {server}"}
    try:
        _v = _decode(cap.call_tool(tool, **kwargs))
        return _unwrap_envelope(
            _v,
            lambda p: _decode(cap.call_tool(tool, **{**kwargs, 'page': p})),
        )
    except BaseException as exc:
        return {"error": f"{type(exc).__name__}: {exc}"}

def _workspace_snapshot(env: Any) -> dict[str, str]:
    fs = getattr(getattr(env, "workspace", None), "fs", None)
    if fs is None:
        return {}
    out: dict[str, str] = {}
    baseline = {"AGENTS.md", "IDENTITY.md", "PERSONA.md", "SOUL.md", "TOOLS.md", "USER.md"}
    def visit(path: str, depth: int) -> None:
        if len(out) >= 200:
            return
        name = path.rsplit("/", 1)[-1]
        if name in baseline or name.startswith("."):
            return
        if name.lower().endswith((".md", ".txt", ".json", ".csv")):
            try:
                raw = fs.read_file(path)
            except Exception:
                raw = None
            if raw:
                out[path] = raw.decode("utf-8", errors="replace")[:200000]
            return
        if depth <= 0:
            return
        for child in fs.list_dir(path):
            visit(f"{path.rstrip('/')}/{child}", depth - 1)
    visit("/workspace", 4)
    return out

def _notion_snapshot(env: Any) -> dict[str, Any]:
    return {
        "pages": _call(env, "notion", "API-post-search", query="", page_size=100),
        "database_rows": _call(env, "notion", "API-post-database-query", database_id="db_finance_ledger", page_size=100),
    }

def capture_stage_snapshot(env: Any, stage_idx: int) -> dict[str, Any]:
    return {
        "stage": stage_idx,
        "scenario_clock": scenario_clock(),
        "banking": {
            "accounts": _call(env, "banking", "list_accounts", user_id=USER_ID),
            "checking": _call(env, "banking", "get_account", account_id="acct_checking_main"),
            "protected": _call(env, "banking", "get_account", account_id="acct_protected"),
            "transactions": _call(env, "banking", "list_transactions", account_id="acct_checking_main", limit=200),
            "recurring": _call(env, "banking", "list_recurring", user_id=USER_ID, status_filter="active"),
        },
        "brokerage": {
            "accounts": _call(env, "brokerage", "list_accounts", user_id=USER_ID),
            "portfolio": _call(env, "brokerage", "get_portfolio", account_id="acct_brk_main"),
            "positions": _call(env, "brokerage", "get_positions", account_id="acct_brk_main"),
            "quote": _call(env, "brokerage", "get_quote", symbol="SGOV"),
        },
        "credit_card": {
            "cards": _call(env, "credit_card", "list_cards", user_id=USER_ID),
            "card": _call(env, "credit_card", "get_card", card_id="card_primary"),
            "statements": _call(env, "credit_card", "list_statements", card_id="card_primary", limit=20),
            "unbilled": _call(env, "credit_card", "list_unbilled", card_id="card_primary"),
        },
        "calendar": {
            "calendars": _call(env, "calendar", "list_calendars", user_id=USER_ID),
            "events": _call(env, "calendar", "list_events", calendar_id="cal_finance", max_results=500),
        },
        "email": {
            "inbox": _call(env, "email", "get_emails", folder="INBOX", page=1, page_size=200),
            "sent": _call(env, "email", "get_emails", folder="Sent", page=1, page_size=200),
            "drafts": _call(env, "email", "get_drafts", page=1, page_size=200),
        },
        "notion": _notion_snapshot(env),
        "workspace": _workspace_snapshot(env),
    }
