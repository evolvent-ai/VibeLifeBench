"""Capture all task backends and the agent workspace at a stage boundary."""
from __future__ import annotations

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Any

WORLD_CLOCK_FILE = Path(os.environ.get("WORLD_CLOCK_FILE", "/world-clock/current.json"))
WORLD_CLOCK_REQUIRED = os.environ.get("WORLD_CLOCK_REQUIRED", "0") == "1"
USER_ID = "usr_yh_q7vkma"
BASELINE = {"AGENTS.md", "IDENTITY.md", "PERSONA.md", "SOUL.md", "TOOLS.md", "USER.md"}

def scenario_clock() -> dict[str, Any]:
    try:
        payload = json.loads(WORLD_CLOCK_FILE.read_text(encoding="utf-8"))
        if set(payload) != {"schema_version", "step", "now"}:
            raise ValueError("clock keys must be exact")
        parsed = datetime.fromisoformat(str(payload["now"]).replace("Z", "+00:00"))
        if parsed.tzinfo is None:
            raise ValueError("clock timestamp has no timezone")
        return {"schema_version": 1, "step": str(payload["step"]), "now": parsed.isoformat()}
    except Exception as exc:
        if WORLD_CLOCK_REQUIRED:
            raise RuntimeError(f"required world clock unavailable: {exc}") from exc
        return {"schema_version": 1, "step": "unknown", "now": ""}

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
    if not isinstance(rows, list) or ("total" not in value and "has_more" not in value):
        return value
    merged = list(rows)
    total = value.get("total")
    page = int(value.get("page") or 1)
    page_size = int(value.get("page_size") or max(1, len(rows)) or 1)
    incomplete = False
    while value.get("has_more") and fetch_page is not None and (total is None or len(merged) < int(total)):
        page += 1
        nxt = fetch_page(page)
        if not isinstance(nxt, dict) or not isinstance(nxt.get("items"), list):
            incomplete = True
            break
        fresh = nxt["items"]
        if not fresh:
            incomplete = True
            break
        merged.extend(fresh)
        value = nxt
        if len(merged) > 10000:
            incomplete = True
            break
    if total is not None and len(merged) < int(total):
        incomplete = True
    return {"items": merged, "total": total if total is not None else len(merged), "captured_complete": not incomplete}

def _call(env: Any, server: str, tool: str, **kwargs: Any) -> Any:
    cap = getattr(env, f"{server}_mock", None)
    if cap is None:
        return {"error": f"missing capability: {server}"}
    try:
        value = _decode(cap.call_tool(tool, **kwargs))
        return _unwrap_envelope(value, lambda p: _decode(cap.call_tool(tool, **{**kwargs, "page": p})))
    except BaseException as exc:
        return {"error": f"{type(exc).__name__}: {exc}"}

def _workspace_snapshot(env: Any) -> dict[str, str]:
    fs = getattr(getattr(env, "workspace", None), "fs", None)
    if fs is None:
        return {}
    out: dict[str, str] = {}
    def visit(path: str, depth: int) -> None:
        if len(out) >= 200 or depth < 0:
            return
        name = path.rsplit("/", 1)[-1]
        if name in BASELINE or name.startswith("."):
            return
        try:
            children = fs.list_dir(path)
        except Exception:
            children = []
        if children:
            for child in children:
                visit(f"{path.rstrip('/')}/{child}", depth - 1)
            return
        if not name.lower().endswith((".md", ".txt", ".json", ".csv")):
            return
        try:
            raw = fs.read_file(path)
            text = raw.decode("utf-8", errors="replace") if isinstance(raw, bytes) else str(raw)
            if text.strip():
                out[path] = text[:200000]
        except Exception:
            return
    visit("/workspace", 4)
    return out

def _server_snapshot(env: Any, server: str) -> dict[str, Any]:
    calls: dict[str, tuple[str, dict[str, Any]]] = {
        "calendar": ("list_events", {"max_results": 500}),
        "credit_card": ("list_cards", {"user_id": USER_ID}),
        "email": ("get_emails", {"folder": "INBOX", "page": 1, "page_size": 50}),
        "maps": ("search_places", {"query": "Shanghai Jing'an alcohol-free celebration", "limit": 100}),
        "notification_hub": ("list_notifications", {"user_id": USER_ID, "limit": 500}),
        "notion": ("API-post-search", {"query": "", "page_size": 100}),
        "review_platform": ("search_merchants", {"category": "venue", "city": "Shanghai", "area": "Jing'an District", "limit": 100}),
    }
    tool, kwargs = calls[server]
    result = {"listing": _call(env, server, tool, **kwargs)}
    return result

def capture_stage_snapshot(env: Any, stage_idx: int) -> dict[str, Any]:
    return {
        "stage": stage_idx,
        "scenario_clock": scenario_clock(),
        **{server: _server_snapshot(env, server) for server in ("calendar", "credit_card", "email", "maps", "notification_hub", "notion", "review_platform")},
        "workspace": _workspace_snapshot(env),
    }
