"""Capture rental-task world state at each stage boundary."""
from __future__ import annotations
import json, os
from pathlib import Path
from typing import Any

SCENARIO_CLOCK_PATH = Path(os.environ.get("WORLD_CLOCK_FILE", "/world-clock/current.json"))
SCENARIO_CLOCK_REQUIRED = os.environ.get("SCENARIO_CLOCK_REQUIRED", "0") == "1"
USER_ID = "user_linyuan"
LISTINGS = (
    "short_101", "short_102", "short_103",
    "long_201", "long_202", "long_203", "long_204", "long_205",
)
MERCHANTS = ("mer_beijing_a", "mer_beijing_b", "mer_beijing_c")
PLACES = (
    "office_a_nanshan", "office_b_bantian", "place_short_103",
    "place_long_201", "place_long_202", "place_long_203",
    "place_long_204", "place_long_205",
)
BASELINE_WORKSPACE_NAMES = {"AGENTS.md","AUTHORIZATION.md","IDENTITY.md","PERSONA.md","SOUL.md","TOOLS.md","USER.md"}
ALLOWED_WORKSPACE_SUFFIXES = (".md", ".txt", ".json", ".csv")

def scenario_clock() -> dict[str, Any]:
    try:
        payload = json.loads(SCENARIO_CLOCK_PATH.read_text(encoding="utf-8"))
        if not isinstance(payload.get("step"), str) or not isinstance(payload.get("now"), str): raise ValueError("invalid scenario clock payload")
        return {"schema_version": 1, "step": payload["step"], "now": payload["now"]}
    except Exception as exc:
        if SCENARIO_CLOCK_REQUIRED: raise RuntimeError(f"required scenario clock unavailable: {exc}") from exc
        return {"schema_version": 1, "step": "unknown", "now": ""}

def _decode(value: Any) -> Any:
    if isinstance(value, str):
        try: return json.loads(value)
        except json.JSONDecodeError: return value
    return value

def _unwrap_envelope(value: Any, fetch_page=None):
    if not isinstance(value, dict): return value
    rows = value.get("items")
    if not isinstance(rows, list) or ("total" not in value and "has_more" not in value): return value
    merged = list(rows); page = int(value.get("page") or 1); total = int(value.get("total") or 0)
    while value.get("has_more") and fetch_page is not None and len(merged) < total:
        page += 1; nxt = fetch_page(page)
        if not isinstance(nxt, dict) or not isinstance(nxt.get("items"), list) or not nxt["items"]:
            value["_pagination_incomplete"] = True; break
        merged.extend(nxt["items"]); value = nxt
    if total and len(merged) < total: value["_pagination_incomplete"] = True
    return merged

def _call(env: Any, server: str, tool: str, **kwargs: Any) -> Any:
    cap = getattr(env, f"{server}_mock", None)
    if cap is None: return {"error": f"missing capability: {server}"}
    try:
        first = _decode(cap.call_tool(tool, **kwargs))
        return _unwrap_envelope(first, lambda p: _decode(cap.call_tool(tool, **{**kwargs, "page": p})))
    except BaseException as exc: return {"error": f"{type(exc).__name__}: {exc}"}

def _freeze_email_bodies(env, rows) -> None:
    """Freeze the full message body next to each header row.

    ``get_emails`` returns headers only (``include_body=False``), so scoring
    lookups that read ``read_email`` content out of the snapshot would always
    match an empty body. Fetch the ``read_email`` detail per row and merge it
    in; rows already carrying a body, and rows the mock cannot resolve, are
    left untouched.
    """
    for row in rows:
        if not isinstance(row, dict) or row.get("body_text") is not None:
            continue
        email_id = row.get("email_id") or row.get("id")
        if email_id is None:
            continue
        detail = _call(env, "email", "read_email", email_id=str(email_id))
        if isinstance(detail, dict) and str(detail.get("email_id") or detail.get("id") or "") == str(email_id):
            row.update(detail)

def _paged_email(env, folder):
    first = _decode(env.email_mock.call_tool("get_emails", folder=folder, page=1, page_size=50))
    if not isinstance(first, dict): return first
    rows = list(first.get("emails") or []); total = int(first.get("total_results") or len(rows)); page = 1
    while len(rows) < total:
        page += 1; nxt = _decode(env.email_mock.call_tool("get_emails", folder=folder, page=page, page_size=50))
        fresh = (nxt.get("emails") if isinstance(nxt, dict) else []) or []
        if not fresh: first["_pagination_incomplete"] = True; break
        rows.extend(fresh)
    first["emails"] = rows; first["captured_complete"] = len(rows) >= total
    _freeze_email_bodies(env, rows)
    return first

def _workspace_snapshot(env):
    fs = getattr(getattr(env, "workspace", None), "fs", None); out = {}
    if fs is None: return out
    def visit(path, depth):
        if len(out) >= 200: return
        name = path.rsplit("/",1)[-1]
        if name in BASELINE_WORKSPACE_NAMES or name.startswith("."): return
        if name.lower().endswith(ALLOWED_WORKSPACE_SUFFIXES):
            try: raw = fs.read_file(path)
            except Exception: return
            text = raw.decode("utf-8", errors="replace") if isinstance(raw, bytes) else str(raw)
            if text.strip(): out[path] = text[:200000]
            return
        if depth > 0:
            for child in fs.list_dir(path): visit(f"{path.rstrip('/')}/{child}", depth-1)
    visit("/workspace", 4); return out


def _notion_snapshot(env) -> dict[str, Any]:
    """Freeze the page, database, row, and block read surfaces used by scoring."""
    pages = _call(
        env, "notion", "API-post-search", query="",
        filter={"value": "page", "property": "object"}, page_size=100,
    )
    databases = _call(
        env, "notion", "API-post-search", query="",
        filter={"value": "database", "property": "object"}, page_size=100,
    )
    page_rows = pages.get("results", []) if isinstance(pages, dict) else []
    database_rows = databases.get("results", []) if isinstance(databases, dict) else []
    rows: dict[str, Any] = {}
    for database in database_rows if isinstance(database_rows, list) else []:
        if not isinstance(database, dict) or not database.get("id"):
            continue
        rows[str(database["id"])] = _call(
            env, "notion", "API-post-database-query",
            database_id=str(database["id"]), page_size=100,
        )
    blocks: dict[str, Any] = {}
    for page in page_rows if isinstance(page_rows, list) else []:
        if not isinstance(page, dict) or not page.get("id"):
            continue
        blocks[str(page["id"])] = _call(
            env, "notion", "API-get-block-children",
            block_id=str(page["id"]), page_size=100,
        )
    return {
        "pages": pages,
        "databases": databases,
        "database_rows": rows,
        "blocks": blocks,
    }

def _shipments_snapshot(env) -> list[Any]:
    """Freeze the full detail of every shipment visible to the user.

    ``list_shipments`` summarizes addresses down to province/city/district and
    drops sender/recipient detail, so scoring lookups that need the full
    address (sender branch, recipient front desk) would always miss. Freeze the
    ``get_shipment`` detail per row and fall back to the summary row only when
    the detail read fails.
    """
    listing = _call(env, "delivery_logistics", "list_shipments", user_id=USER_ID, limit=100)
    rows = listing if isinstance(listing, list) else []
    out: list[Any] = []
    for row in rows:
        if not isinstance(row, dict) or not row.get("shipment_id"):
            continue
        detail = _call(env, "delivery_logistics", "get_shipment", shipment_id=str(row["shipment_id"]))
        out.append(detail if isinstance(detail, dict) and detail.get("shipment_id") else row)
    return out


JOBS = ("onboard_pm_001",)

def _jobs_snapshot(env) -> list[Any]:
    """Freeze the job catalog without a language-bound keyword filter.

    ``search_jobs`` matches title/jd/requirements/tags with a LIKE filter; a
    keyword that no seed row contains freezes an empty corpus. Enumerate all
    open jobs with an empty keyword and pin the full ``get_job`` detail (jd and
    requirements are search-view omissions) for the jobs scoring reads.
    """
    out: list[Any] = []
    for job_id in JOBS:
        detail = _call(env, "job_board", "get_job", job_id=job_id)
        if isinstance(detail, dict) and detail.get("job_id"):
            out.append(detail)
    catalog = _call(env, "job_board", "search_jobs", keyword="", limit=100)
    if isinstance(catalog, list):
        pinned = {str(row.get("job_id")) for row in out}
        out.extend(
            row for row in catalog
            if isinstance(row, dict) and row.get("job_id") and str(row["job_id"]) not in pinned
        )
    return out


def capture_stage_snapshot(env: Any, stage_idx: int) -> dict[str, Any]:
    return {
        "stage": stage_idx, "scenario_clock": scenario_clock(),
        "listing_platform": {"listings": {i: _call(env,"listing_platform","get_listing_detail",listing_id=i) for i in LISTINGS}, "saved": _call(env,"listing_platform","list_saved",user_id=USER_ID), "viewings": _call(env,"listing_platform","list_viewings",user_id=USER_ID)},
        "maps": {"places": {i: _call(env,"maps","get_place_details",place_id=i) for i in PLACES}},
        "email": {"inbox": _paged_email(env,"INBOX"), "sent": _paged_email(env,"Sent"), "drafts": _call(env,"email","get_drafts",page_size=100)},
        "calendar": {"events": _call(env,"calendar","list_events",calendar_id="cal_linyuan_main",max_results=500)},
        "delivery_logistics": {"shipments": _shipments_snapshot(env)},
        "job_board": {"jobs": _jobs_snapshot(env)},
        "notification_hub": {"notifications": _call(env,"notification_hub","list_notifications",user_id=USER_ID,limit=500)},
        "notion": _notion_snapshot(env),
        "workspace": _workspace_snapshot(env),
    }
