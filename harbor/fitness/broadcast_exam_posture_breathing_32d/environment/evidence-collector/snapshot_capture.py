"""Task-specific stage snapshot capture for the five vendored services."""
from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

WORLD_CLOCK_FILE = Path(os.environ.get("WORLD_CLOCK_FILE", "/world-clock/current.json"))
WORLD_CLOCK_REQUIRED = os.environ.get("WORLD_CLOCK_REQUIRED", "0") == "1"


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


def _workspace(env: Any) -> dict[str, Any]:
    names = env.workspace.fs.list_dir("/workspace")
    return {"files": names, "readable": bool(names)}


def capture_stage_snapshot(env: Any, stage_idx: int) -> dict[str, Any]:
    """Capture live backend state at a virtual-stage boundary."""
    return {
        "stage": stage_idx,
        "world_clock": world_clock(),
        "calendar": {"calendars": _call(env, "calendar", "list_calendars", user_id="lin_yu"),
                      "events": _call(env, "calendar", "list_events", calendar_id="cal_linyu_broadcast", max_results=500)},
        "email": {"inbox": _call(env, "email", "get_emails", folder="INBOX", page=1, page_size=250),
                   "sent": _call(env, "email", "get_emails", folder="Sent", page=1, page_size=250),
                   "drafts": _call(env, "email", "get_drafts", page=1, page_size=200)},
        "health_tracker": {"sleep": _call(env, "health_tracker", "get_metrics", user_id="lin_yu", type="sleep_minutes", limit=500),
                            "workouts": _call(env, "health_tracker", "list_workouts", user_id="lin_yu", limit=500),
                            "heart_rate": _call(env, "health_tracker", "get_metrics", user_id="lin_yu", type="heart_rate", limit=100)},
        "notion": {"search": _call(env, "notion", "API-post-search", page_size=100),
                    "self": _call(env, "notion", "API-get-self")},
        "weather": {"alerts": _call(env, "weather", "get_alerts", geo="beijing_broadcast_campus"),
                     "daily": _call(env, "weather", "get_forecast_daily", geo="beijing_broadcast_campus"),
                     "hourly": _call(env, "weather", "get_forecast_hourly", geo="beijing_broadcast_campus")},
        "workspace": _workspace(env),
    }
