"""Capture rental-task world state at each stage boundary."""
from __future__ import annotations
import json, os
from pathlib import Path
from typing import Any

SCENARIO_CLOCK_PATH = Path(os.environ.get("WORLD_CLOCK_FILE", "/world-clock/current.json"))
SCENARIO_CLOCK_REQUIRED = os.environ.get("SCENARIO_CLOCK_REQUIRED", "0") == "1"
USER_ID = "usr_foreign_018"
LISTINGS = ("rs018_listing_a", "rs018_listing_b", "rs018_listing_c", "rs018_listing_d")
MERCHANTS = ("mer_beijing_a", "mer_beijing_b", "mer_beijing_c")
PLACES = ("pl_beijing_lab_office", "pl_beijing_a", "pl_beijing_b", "pl_beijing_c")
BASELINE_WORKSPACE_NAMES = {
    "ACCOUNT_CONTEXT.md",
    "AGENTS.md",
    "ARTIFACT_CONTRACT.md",
    "AUTHORIZATION.md",
    "BUDGET_LEDGER.md",
    "CONTACT_TRUST_TEMPLATE.md",
    "IDENTITY.md",
    "LEASE_CHECKLIST_TEMPLATE.md",
    "MATERIAL_DISCLOSURE_TEMPLATE.md",
    "PERSONA.md",
    "PRIVACY_POLICY.md",
    "RENTAL_REQUIREMENTS.md",
    "SOUL.md",
    "TOOLS.md",
    "TRACKER_TEMPLATE.md",
    "USER.md",
}
ALLOWED_WORKSPACE_SUFFIXES = (".md", ".txt", ".json", ".csv")

def scenario_clock() -> dict[str, Any]:
    try:
        payload = json.loads(SCENARIO_CLOCK_PATH.read_text(encoding="utf-8"))
        if set(payload) != {"world_now"} or not isinstance(payload.get("world_now"), str):
            raise ValueError("invalid world clock payload")
        return {"schema_version": 1, "now": payload["world_now"]}
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

def _paged_email(env, folder):
    first = _decode(env.email_mock.call_tool("get_emails", folder=folder, page=1, page_size=50))
    if not isinstance(first, dict): return first
    rows = list(first.get("emails") or []); total = int(first.get("total_results") or len(rows)); page = 1
    while len(rows) < total:
        page += 1; nxt = _decode(env.email_mock.call_tool("get_emails", folder=folder, page=page, page_size=50))
        fresh = (nxt.get("emails") if isinstance(nxt, dict) else []) or []
        if not fresh: first["_pagination_incomplete"] = True; break
        rows.extend(fresh)
    if folder.upper() == "INBOX":
        enriched = []
        for row in rows:
            item = dict(row) if isinstance(row, dict) else row
            email_id = str(item.get("email_id") or item.get("id") or "") if isinstance(item, dict) else ""
            if email_id in {"1", "2", "3", "214", "215"}:
                detail = _call(env, "email", "read_email", email_id=email_id)
                if isinstance(detail, dict) and "error" not in detail:
                    item.update(detail)
            enriched.append(item)
        rows = enriched
    return rows

def _notion_snapshot(env):
    pages = _call(env, "notion", "API-post-search", query="", filter={"value": "page", "property": "object"}, page_size=100)
    page_rows = pages.get("results", []) if isinstance(pages, dict) else pages
    blocks = {}
    for page in page_rows if isinstance(page_rows, list) else []:
        if isinstance(page, dict) and page.get("id"):
            blocks[str(page["id"])] = _call(env, "notion", "API-get-block-children", block_id=str(page["id"]), page_size=10000)
    return {"pages": pages, "blocks": blocks}

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

def capture_stage_snapshot(env: Any, stage_idx: int) -> dict[str, Any]:
    return {
        "stage": stage_idx, "scenario_clock": scenario_clock(),
        "listing_platform": {"listings": {i: _call(env,"listing_platform","get_listing_detail",listing_id=i) for i in LISTINGS}, "saved": _call(env,"listing_platform","list_saved",user_id=USER_ID), "viewings": _call(env,"listing_platform","list_viewings",user_id=USER_ID)},
        "maps": {"places": {i: _call(env,"maps","get_place_details",place_id=i) for i in PLACES}},
        "email": {"inbox": _paged_email(env,"INBOX"), "sent": _paged_email(env,"Sent"), "drafts": _call(env,"email","get_drafts",page_size=100)},
        "calendar": {"events": _call(env,"calendar","list_events",calendar_id="cal_nurse_main",max_results=500)},
        "review_platform": {"reviews": {i: _call(env,"review_platform","list_reviews",merchant_id=i,limit=100) for i in MERCHANTS}},
        "legal_search": {"cases": _call(env,"legal_search","search_cases",query="rental",limit=100)},
        "notification_hub": {"notifications": _call(env,"notification_hub","list_notifications",user_id=USER_ID,limit=500)},
        "notion": _notion_snapshot(env),
        "workspace": _workspace_snapshot(env),
    }
