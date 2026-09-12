"""Freeze the seven pottery-task service states at each stage boundary."""
from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

WORLD_CLOCK_FILE = Path(os.environ.get("WORLD_CLOCK_FILE", "/world-clock/current.json"))
WORLD_CLOCK_REQUIRED = os.environ.get("WORLD_CLOCK_REQUIRED", "0") == "1"
USER_ID = "user_luyao_tb011"
CARD_ID = "card_luyao_team_corp"
LUMEN_ID = "venue_pottery_lumen_heping"
SOUTHBANK_ID = "venue_pottery_southbank"
PLACE_IDS = ("place_pottery_lumen_heping", "place_pottery_southbank")


def world_clock() -> dict[str, Any]:
    try:
        payload = json.loads(WORLD_CLOCK_FILE.read_text(encoding="utf-8"))
        if set(payload) != {"world_now"}:
            raise ValueError("invalid world clock payload")
        return {"schema_version": 1, "world_now": str(payload["world_now"])}
    except Exception as exc:
        if WORLD_CLOCK_REQUIRED:
            raise RuntimeError(f"required world clock unavailable: {exc}") from exc
        return {"schema_version": 1, "world_now": ""}


def _decode(value: Any) -> Any:
    """Convert MCP SDK results into JSON-native values before persistence."""
    if isinstance(value, bytes):
        return value.decode("utf-8", errors="replace")
    if isinstance(value, str):
        try:
            return json.loads(value)
        except json.JSONDecodeError:
            return value
    structured = getattr(value, "structuredContent", None)
    if structured is None:
        structured = getattr(value, "structured_content", None)
    if isinstance(structured, dict):
        return _decode(structured.get("result", structured))
    content = getattr(value, "content", None)
    if content is not None:
        for block in content or []:
            if bool(getattr(block, "isError", False)) or bool(getattr(block, "is_error", False)):
                return {"error": str(getattr(block, "text", "MCP content block error"))}
            text = getattr(block, "text", None)
            if text is not None:
                return _decode(text)
        if content == []:
            return []
    # Pydantic MCP models expose model_dump; use it as a final serialization
    # fallback for result variants without structured content or text blocks.
    model_dump = getattr(value, "model_dump", None)
    if callable(model_dump):
        try:
            return _decode(model_dump(mode="json"))
        except TypeError:
            return _decode(model_dump())
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


def _workspace(env: Any) -> dict[str, Any]:
    files: dict[str, str] = {}
    for name in env.workspace.fs.list_dir("/workspace"):
        if name.startswith("."):
            continue
        try:
            files[name] = _decode(env.workspace.fs.read_file(f"/workspace/{name}"))
        except (FileNotFoundError, PermissionError):
            continue
    return {"files": files, "readable": bool(files)}


def _notion(env: Any) -> dict[str, Any]:
    pages = _call(env, "notion", "API-post-search", query="", filter={"value": "page"}, page_size=100)
    authored = _call(env, "notion", "API-post-search", query="Pottery planning stage", filter={"value": "page"}, page_size=100)
    page_rows: list[Any] = []
    for result in (pages, authored):
        rows = result.get("results", []) if isinstance(result, dict) else result
        if isinstance(rows, list):
            page_rows.extend(rows)
    page_map: dict[str, Any] = {}
    block_map: dict[str, Any] = {}
    seen: set[str] = set()
    for row in page_rows:
        if not isinstance(row, dict):
            continue
        page_id = str(row.get("id") or row.get("page_id") or "")
        if not page_id or page_id in seen:
            continue
        seen.add(page_id)
        page_map[page_id] = _call(env, "notion", "API-retrieve-a-page", page_id=page_id)
        block_map[page_id] = _call(env, "notion", "API-get-block-children", block_id=page_id, page_size=100)
    return {
        "pages": pages,
        "authored_pages": authored,
        "self": _call(env, "notion", "API-get-self"),
        "API-retrieve-a-page": page_map,
        "API-get-block-children": block_map,
    }


def _review_platform(env: Any) -> dict[str, Any]:
    merchants = _call(
        env,
        "review_platform",
        "search_merchants",
        category="venue",
        city="Tianjin",
        area="Heping",
        limit=100,
    )
    merchant_details = {
        LUMEN_ID: _call(env, "review_platform", "get_merchant", merchant_id=LUMEN_ID),
        SOUTHBANK_ID: _call(env, "review_platform", "get_merchant", merchant_id=SOUTHBANK_ID),
    }
    return {
        "search_merchants": merchants,
        "merchants": merchant_details,
        "merchant_qa": {
            LUMEN_ID: _call(env, "review_platform", "get_merchant_qa", merchant_id=LUMEN_ID),
            SOUTHBANK_ID: _call(env, "review_platform", "get_merchant_qa", merchant_id=SOUTHBANK_ID),
        },
        "list_reservations": _call(env, "review_platform", "list_reservations", user_id=USER_ID),
    }


def _maps(env: Any) -> dict[str, Any]:
    return {
        "places": _call(env, "maps", "search_places", query="Tianjin Heping pottery", limit=100),
        "get_place_details": {
            place_id: _call(env, "maps", "get_place_details", place_id=place_id)
            for place_id in PLACE_IDS
        },
    }


def capture_stage_snapshot(env: Any, stage_idx: int) -> dict[str, Any]:
    """Capture live backend state at a virtual-stage boundary."""
    return {
        "stage": stage_idx,
        "world_clock": world_clock(),
        "calendar": {
            "calendars": _call(env, "calendar", "list_calendars", user_id=USER_ID),
            "events": _call(env, "calendar", "list_events", calendar_id="cal_luyao_team", max_results=500),
        },
        "email": {
            "inbox": _call(env, "email", "get_emails", folder="INBOX", page=1, page_size=250),
            "sent": _call(env, "email", "get_emails", folder="Sent", page=1, page_size=250),
            "drafts": _call(env, "email", "get_drafts", page=1, page_size=200),
        },
        "notification_hub": {
            "list_notifications": _call(env, "notification_hub", "list_notifications", user_id=USER_ID, limit=500),
        },
        "notion": _notion(env),
        "review_platform": _review_platform(env),
        "maps": _maps(env),
        "credit_card": {
            "cards": _call(env, "credit_card", "list_cards", user_id=USER_ID),
            "get_card": _call(env, "credit_card", "get_card", card_id=CARD_ID),
            "unbilled": _call(env, "credit_card", "list_unbilled", card_id=CARD_ID),
            "statements": _call(env, "credit_card", "list_statements", card_id=CARD_ID, limit=12),
            "payments": [],
        },
        "workspace": _workspace(env),
    }
