"""Freeze the Japan family-trip world through all task MCP services."""
from __future__ import annotations
import json, os
from datetime import datetime
from pathlib import Path
from typing import Any

USER_ID = "li_wei"
CALENDAR_ID = "cal_000001"
NOTION_PAGE_ID = "aaaaaaaa-aaaa-4aaa-8aaa-000000000001"
CLOCK = Path(os.environ.get("WORLD_CLOCK_FILE", "/world-clock/current.json"))
BASELINE = {"AGENTS.md", "ARTIFACT_CONTRACT.md", "IDENTITY.md", "PERSONA.md", "SOUL.md", "TOOLS.md", "USER.md"}

def _decode(value: Any) -> Any:
    if isinstance(value, str):
        try: return json.loads(value)
        except json.JSONDecodeError: return value
    return value

def _unwrap_envelope(value: Any, fetch_page=None) -> Any:
    if not isinstance(value, dict): return value
    rows = value.get("items")
    if not isinstance(rows, list) or ("total" not in value and "has_more" not in value): return value
    merged = list(rows); total = value.get("total"); total = int(total) if isinstance(total, (int,float)) else None
    page = int(value.get("page") or 1); current = value
    while fetch_page is not None and current.get("has_more"):
        page += 1; nxt = fetch_page(page)
        if not isinstance(nxt, dict) or not isinstance(nxt.get("items"), list) or not nxt["items"]: break
        merged.extend(nxt["items"]); current = nxt
        if total is not None and len(merged) >= total: break
    if (total is not None and len(merged) < total) or current.get("has_more"):
        return {"items": merged, "_pagination_incomplete": True, "_captured": len(merged), "_total": total}
    return merged

def _call(env: Any, server: str, tool: str, **kwargs: Any) -> Any:
    cap = getattr(env, f"{server}_mock", None)
    if cap is None: return {"error": f"missing capability: {server}"}
    try:
        first = _decode(cap.call_tool(tool, **kwargs))
        return _unwrap_envelope(first, lambda page: _decode(cap.call_tool(tool, **{**kwargs, "page": page})))
    except BaseException as exc:
        return {"error": f"{type(exc).__name__}: {exc}"}

def _paged_call(env, server, tool, *, rows_key, id_keys, **kwargs):
    first = _call(env, server, tool, page=1, page_size=50, **kwargs)
    if not isinstance(first, dict) or first.get("error"): return first
    rows = list(first.get(rows_key) or []); raw = first.get("total_results", first.get("total", len(rows)))
    total = int(raw) if isinstance(raw, (int,float)) else len(rows)
    def rid(row): return next((str(row[k]) for k in id_keys if isinstance(row, dict) and row.get(k) is not None), "")
    seen = {rid(r) for r in rows}; page = 2
    while len(rows) < total:
        nxt = _call(env, server, tool, page=page, page_size=50, **kwargs)
        if not isinstance(nxt, dict) or nxt.get("error"): break
        fresh = [r for r in (nxt.get(rows_key) or []) if rid(r) not in seen]
        if not fresh: break
        rows.extend(fresh); seen.update(rid(r) for r in fresh); page += 1
    first[rows_key] = rows; first["captured_count"] = len(rows); first["captured_complete"] = len(rows) >= total
    return first

def _email(env, folder, details=False):
    listing = _paged_call(env, "email", "get_emails", rows_key="emails", id_keys=("email_id","id"), folder=folder)
    out = {}
    if details and isinstance(listing, dict):
        for row in listing.get("emails") or []:
            eid = row.get("email_id") or row.get("id") if isinstance(row, dict) else None
            if eid is None: continue
            detail = _call(env, "email", "read_email", email_id=str(eid)); headers = _call(env, "email", "get_email_headers", email_id=str(eid))
            if isinstance(detail, dict) and isinstance(headers, dict):
                for k in ("in_reply_to","references","thread_id"):
                    if headers.get(k) is not None: detail.setdefault(k, headers[k])
            out[str(eid)] = detail
    return {"listing": listing, "details": out}

def _workspace(env):
    fs = getattr(getattr(env, "workspace", None), "fs", None)
    if fs is None: return {}
    out = {}; seen = set()
    def walk(path, depth):
        if path in seen or len(out) >= 200: return
        seen.add(path); name = path.rsplit("/",1)[-1]
        if name.startswith(".") or name in BASELINE: return
        if name.lower().endswith((".md",".txt",".json",".csv")):
            try: raw = fs.read_file(path)
            except Exception: return
            text = raw.decode("utf-8", "replace") if isinstance(raw, bytes) else str(raw)
            if text.strip(): out[path] = text[:200000]
            return
        if depth:
            try:
                for child in fs.list_dir(path): walk(f"{path.rstrip('/')}/{child}", depth-1)
            except Exception: pass
    walk("/workspace", 4); return out

def _clock():
    payload = json.loads(CLOCK.read_text(encoding="utf-8"))
    if not isinstance(payload, dict) or set(payload) != {"world_now"}: raise RuntimeError("world clock must contain exactly world_now")
    value = payload["world_now"]
    if not isinstance(value, str): raise RuntimeError("world_now must be a string")
    if datetime.fromisoformat(value.replace("Z", "+00:00")).tzinfo is None: raise RuntimeError("world_now must include a timezone")
    return {"world_now": value}

def _list_details(env, server, list_tool, detail_tool, list_key, id_key, **kwargs):
    listing = _call(env, server, list_tool, **kwargs)
    if isinstance(listing, list):
        rows = listing
    elif isinstance(listing, dict):
        rows = listing.get(list_key, [])
        # hotel_booking.list_reservations returns reservation_ids, while the
        # generic collector historically looked only for reservations.
        if not rows and list_key == "reservations":
            rows = listing.get("reservation_ids", [])
    else:
        rows = []
    details = {}
    for row in rows or []:
        ident = row.get(id_key) if isinstance(row, dict) else row
        if ident: details[str(ident)] = _call(env, server, detail_tool, **{id_key: str(ident)})
    return {"listing": listing, "details": details}

def _notion(env):
    search = _call(env, "notion", "API-post-search", query="Japan Trip Journal", page_size=100)
    pages = search.get("results", []) if isinstance(search, dict) else []
    if not pages: pages = [_call(env, "notion", "API-retrieve-a-page", page_id=NOTION_PAGE_ID)]
    return {"search": search, "pages": pages, "blocks": {str(p.get("id")): _call(env,"notion","API-get-block-children",block_id=str(p.get("id")),page_size=100) for p in pages if isinstance(p,dict) and p.get("id")}}

def capture_stage_snapshot(env: Any, stage_idx: int) -> dict[str, Any]:
    return {
        "stage": int(stage_idx), "world_clock": _clock(), "workspace": _workspace(env),
        "flight_booking": _list_details(env,"flight_booking","list_bookings","get_booking","bookings","pnr",user_id=USER_ID),
        "hotel_booking": _list_details(env,"hotel_booking","list_reservations","get_reservation","reservations","reservation_id",user_id=USER_ID),
        "visa_and_advisory": {"applications": _call(env,"visa_and_advisory","list_visa_applications",user_id=USER_ID), "entry_requirements": _call(env,"visa_and_advisory","check_entry_requirements",nationality="CN",destination="JP",purpose="tourism")},
        "calendar": {"events": _call(env,"calendar","list_events",calendar_id=CALENDAR_ID,max_results=500)},
        "email": {"inbox": _email(env,"INBOX"), "sent": _email(env,"Sent",True), "drafts": _paged_call(env,"email","get_drafts",rows_key="drafts",id_keys=("draft_id","id"))},
        "maps": {"places": _call(env,"maps","search_places",query="Japan")},
        "weather": {"forecasts": _call(env,"weather","get_forecast",location="Tokyo"), "alerts": _call(env,"weather","list_alerts",location="Tokyo")},
        "notion": _notion(env),
    }
