"""Read-only stage snapshots for the litigation task."""
from __future__ import annotations
import json, os
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from pathlib import Path
from typing import Any

WORLD_CLOCK_FILE = Path(os.environ.get("WORLD_CLOCK_FILE", "/world-clock/current.json"))

def scenario_clock() -> dict[str, Any]:
    try:
        payload = json.loads(WORLD_CLOCK_FILE.read_text(encoding="utf-8"))
        if not isinstance(payload, dict) or set(payload) != {"world_now"}:
            raise ValueError("clock keys must be exactly {'world_now'}")
        value = payload["world_now"]
        parsed = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
        if parsed.tzinfo is None or parsed.utcoffset() is None: raise ValueError("clock must include an offset")
        return {"schema_version": 1, "now": str(value)}
    except Exception as exc:
        raise RuntimeError(f"required world clock unavailable at {WORLD_CLOCK_FILE}: {exc}") from exc

def _decode(value: Any) -> Any:
    if isinstance(value, str):
        try: return json.loads(value)
        except json.JSONDecodeError: return value
    return value

def _unwrap_envelope(value: Any, fetch_page=None) -> Any:
    if not isinstance(value, dict): return value
    rows = value.get("items")
    if not isinstance(rows, list) or ("total" not in value and "has_more" not in value): return value
    merged, total, page = list(rows), value.get("total"), int(value.get("page") or 1) + 1
    complete = True
    while fetch_page is not None and value.get("has_more") and page <= 100:
        nxt = fetch_page(page)
        if not isinstance(nxt, dict) or not isinstance(nxt.get("items"), list): complete = False; break
        merged.extend(nxt["items"]); value = nxt; page += 1
        if isinstance(total, int) and len(merged) >= total: break
    if value.get("has_more") or not complete:
        return {"error": "capture pagination did not complete"}
    return merged


CAPTURE_WORKERS = 12

def _parallel_calls(env: Any, jobs: list[Any]) -> list[Any]:
    """Run independent read-only MCP captures concurrently, in job order.

    A stage boundary must freeze the whole world inside Harbor's 60s collect-hook
    budget; the Notion block-children and Maps place-details fans out to hundreds
    of single-round-trip calls, which is only feasible when they overlap.
    """
    if len(jobs) <= 1:
        return [job() for job in jobs]
    workers = min(CAPTURE_WORKERS, len(jobs))
    with ThreadPoolExecutor(max_workers=workers) as pool:
        return list(pool.map(lambda job: job(), jobs))

def _capture_error(value: Any, server: str, tool: str) -> dict[str, str] | None:
    if not isinstance(value, dict):
        return None
    failed = (
        value.get("isError") is True
        or value.get("is_error") is True
        or value.get("ok") is False
        or str(value.get("status") or "").lower() in {"error", "failed", "failure"}
        or bool(value.get("error"))
    )
    if not failed:
        return None
    detail = value.get("error") or value.get("message") or value
    code = value.get("code")
    suffix = f" ({code})" if code else ""
    return {"error": f"{server}.{tool}: {detail}{suffix}"}

def _call(env: Any, server: str, tool: str, **kwargs: Any) -> Any:
    cap = getattr(env, f"{server}_mock", None)
    if cap is None: return {"error": f"missing capability: {server}"}
    try:
        value = _decode(cap.call_tool(tool, **kwargs))
        error = _capture_error(value, server, tool)
        if error is not None:
            return error
        unwrapped = _unwrap_envelope(value, lambda p: _decode(cap.call_tool(tool, **{**kwargs, "page": p})))
        return _capture_error(unwrapped, server, tool) or unwrapped
    except BaseException as exc: return {"error": f"{type(exc).__name__}: {exc}"}

def _paged_call(env: Any, server: str, tool: str, rows_key: str, id_keys: tuple[str, ...], **kwargs: Any) -> Any:
    call_kwargs = dict(kwargs)
    call_kwargs.setdefault("page", 1)
    call_kwargs.setdefault("page_size", 50)
    first = _call(env, server, tool, **call_kwargs)
    if not isinstance(first, dict) or not isinstance(first.get(rows_key), list): return first
    total = first.get("total_results", first.get("total_drafts", first.get("total")))
    merged, seen, page, current = [], set(), int(first.get("current_page") or first.get("page") or 1), first
    while True:
        for row in current.get(rows_key, []):
            key = next((row.get(k) for k in id_keys if isinstance(row, dict) and row.get(k) is not None), json.dumps(row, sort_keys=True))
            if key not in seen: seen.add(key); merged.append(row)
        total_pages = current.get("total_pages")
        has_more = bool(current.get("has_more")) or (
            isinstance(total_pages, int) and page < total_pages
        ) or (isinstance(total, int) and len(merged) < total)
        if not has_more or (isinstance(total, int) and len(merged) >= total): break
        page += 1
        current = _call(env, server, tool, **{**call_kwargs, "page": page})
        if not isinstance(current, dict) or not isinstance(current.get(rows_key), list):
            return {"error": f"{server}.{tool}: capture pagination did not complete"}
    return {**first, rows_key: merged, "captured_complete": True}

def _email_snapshot(env: Any, folder: str) -> Any:
    return _paged_call(env, "email", "get_emails", "emails", ("id", "email_id", "message_id"), folder=folder)

def _workspace_snapshot(env: Any) -> dict[str, str]:
    fs = getattr(getattr(env, "workspace", None), "fs", None)
    if fs is None:
        raise RuntimeError("workspace capture capability is unavailable")
    out = {}
    def visit(path: str, depth: int) -> None:
        if depth < 0 or len(out) >= 200: return
        children = fs.list_dir(path)
        for child in children:
            p = f"{path.rstrip('/')}/{child}"
            if child.startswith(".") or child in {"AGENTS.md", "IDENTITY.md", "PERSONA.md", "SOUL.md", "TOOLS.md", "USER.md"}: continue
            if child.endswith((".md", ".txt", ".json", ".csv")):
                raw = fs.read_file(p); text = raw.decode("utf-8", errors="replace") if isinstance(raw, bytes) else str(raw)
                if text.strip(): out[p] = text[:200000]
            elif depth: visit(p, depth - 1)
    visit("/workspace", 4); return out

def _notion_search_all(env: Any, **kwargs: Any) -> Any:
    """Capture the complete Notion search envelope, following cursors."""
    first = _call(env, "notion", "API-post-search", page_size=100, **kwargs)
    if not isinstance(first, dict) or not isinstance(first.get("results"), list):
        return first
    merged = list(first["results"])
    current = first
    cursor = current.get("next_cursor")
    while current.get("has_more") and cursor:
        current = _call(
            env,
            "notion",
            "API-post-search",
            page_size=100,
            start_cursor=cursor,
            **kwargs,
        )
        if not isinstance(current, dict) or not isinstance(current.get("results"), list):
            return {"error": "notion.API-post-search: capture pagination did not complete"}
        merged.extend(current["results"])
        cursor = current.get("next_cursor")
    if current.get("has_more"):
        return {"error": "notion.API-post-search: capture pagination cursor is missing"}
    return {**first, "results": merged, "has_more": False, "next_cursor": None}


def _notion_snapshot(env: Any) -> dict[str, Any]:
    pages = _notion_search_all(env, query="")
    databases = _notion_search_all(
        env,
        query="",
        filter={"value": "database", "property": "object"},
    )
    page_blocks: dict[str, Any] = {}
    if isinstance(pages, dict):
        page_ids = [
            str(row["id"])
            for row in pages.get("results", [])
            if isinstance(row, dict) and row.get("object") == "page" and row.get("id")
        ]
        blocks = _parallel_calls(
            env,
            [
                lambda page_id=page_id: _call(
                    env,
                    "notion",
                    "API-get-block-children",
                    block_id=page_id,
                    page_size=10000,
                )
                for page_id in page_ids
            ],
        )
        page_blocks = dict(zip(page_ids, blocks))
    return {"pages": pages, "databases": databases, "page_blocks": page_blocks}


def _maps_places_snapshot(env: Any) -> dict[str, Any]:
    """Capture both endpoint searches and their full detail records."""
    gate = _call(env, "maps", "search_places", query="Riverside Court East Gate", limit=100)
    merchant = _call(env, "maps", "search_places", query="Casa Luna Kitchen", limit=100)
    rows: list[Any] = []
    for value in (gate, merchant):
        if isinstance(value, dict) and set(value) == {"error"}:
            return {"places": value, "place_details": {}}
        if isinstance(value, list):
            rows.extend(value)
        elif isinstance(value, dict):
            rows.extend(value.get("items", []))
    unique: dict[str, Any] = {}
    for row in rows:
        if isinstance(row, dict) and row.get("place_id"):
            unique[str(row["place_id"])] = row
    place_ids = list(unique)
    detail_rows = _parallel_calls(
        env,
        [
            lambda place_id=place_id: _call(
                env, "maps", "get_place_details", place_id=place_id
            )
            for place_id in place_ids
        ],
    )
    details = dict(zip(place_ids, detail_rows))
    detail_error = next(
        (value for value in details.values() if isinstance(value, dict) and set(value) == {"error"}),
        None,
    )
    if detail_error is not None:
        return {"places": detail_error, "place_details": details}
    return {"places": list(unique.values()), "place_details": details}

def capture_stage_snapshot(env: Any, stage_idx: int) -> dict[str, Any]:
    places = _maps_places_snapshot(env)
    return {"stage": stage_idx, "scenario_clock": scenario_clock(),
        "delivery_logistics": {"shipments": _call(env,"delivery_logistics","list_shipments",user_id="user_diego_morales",limit=500), "target": _call(env,"delivery_logistics","get_shipment",shipment_id="ship_diego_1842"), "tracking": _call(env,"delivery_logistics","track_package",tracking_no="DL-DGM-0718-1842")},
        "email": {"inbox": _email_snapshot(env,"Inbox"), "sent": _email_snapshot(env,"Sent"), "drafts": _paged_call(env,"email","get_drafts","drafts",("draft_id","id"))},
        "maps": {**places, "directions": _call(env,"maps","directions",origin="Casa Luna Kitchen",dest="Riverside Court East Gate"), "traffic": _call(env,"maps","get_traffic_estimate",origin="Casa Luna Kitchen",dest="Riverside Court East Gate")},
        "legal_search": {"cases": _call(env,"legal_search","search_cases",keyword="witness statement",limit=100), "statutes": _call(env,"legal_search","search_statutes",keyword="electronic data",limit=100), "saved": _call(env,"legal_search","list_saved",user_id="user_diego_morales")}, "notion": _notion_snapshot(env), "workspace": _workspace_snapshot(env)}
