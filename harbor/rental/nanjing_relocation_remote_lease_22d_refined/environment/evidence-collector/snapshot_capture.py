"""Task-specific stage snapshots for the seven rental-verification mocks."""
from __future__ import annotations
import json, os
from pathlib import Path
from typing import Any

SCENARIO_CLOCK_PATH = Path(os.environ.get("WORLD_CLOCK_FILE", "/world-clock/current.json"))
SCENARIO_CLOCK_REQUIRED = True
USER_ID = "usr_gufeng"
BASELINE_WORKSPACE_NAMES = {"AGENTS.md","ARTIFACT_CONTRACT.md","IDENTITY.md","PERSONA.md","SOUL.md","TOOLS.md","USER.md"}
ALLOWED_WORKSPACE_SUFFIXES = (".md", ".txt", ".json", ".csv")

def scenario_clock() -> dict[str, Any]:
    try:
        p = json.loads(SCENARIO_CLOCK_PATH.read_text(encoding="utf-8"))
        now = p["now"]; step = p["step"]
        if not isinstance(now, str) or not isinstance(step, str): raise ValueError("invalid clock")
        return {"schema_version": 1, "step": step, "now": now}
    except Exception as exc:
        if SCENARIO_CLOCK_REQUIRED: raise RuntimeError(f"required world clock unavailable: {exc}") from exc
        return {"schema_version": 1, "step": "unknown", "now": ""}

def _decode(v: Any) -> Any:
    if isinstance(v, str):
        try: return json.loads(v)
        except json.JSONDecodeError: return v
    return v

def _unwrap_envelope(value: Any, fetch_page=None):
    if not isinstance(value, dict): return value
    rows = value.get("items")
    if not isinstance(rows, list) or ("total" not in value and "has_more" not in value): return value
    merged = list(rows); page = int(value.get("page", 1) or 1); total = value.get("total")
    while value.get("has_more") and fetch_page is not None and (not isinstance(total, int) or len(merged) < total):
        page += 1; nxt = fetch_page(page)
        if not isinstance(nxt, dict) or not isinstance(nxt.get("items"), list) or not nxt["items"]:
            merged.append({"_pagination_incomplete": True}); break
        merged.extend(nxt["items"]); value = nxt
        if len(merged) > 10000: merged.append({"_pagination_incomplete": True}); break
    return merged

def _call(env: Any, server: str, tool: str, **kwargs: Any) -> Any:
    cap = getattr(env, f"{server}_mock", None)
    if cap is None: return {"error": f"missing capability: {server}"}
    try:
        value = _decode(cap.call_tool(tool, **kwargs))
        return _unwrap_envelope(value, lambda page: _decode(cap.call_tool(tool, **{**kwargs, "page": page})))
    except BaseException as exc: return {"error": f"{type(exc).__name__}: {exc}"}

def _paged_call(env, server, tool, rows_key, id_keys, **kwargs):
    first = _call(env, server, tool, page=1, page_size=200, **kwargs)
    if not isinstance(first, dict) or not isinstance(first.get(rows_key), list): return first
    rows = list(first[rows_key]); total = first.get("total", first.get("total_results")); page = 1
    while first.get("has_more") or (isinstance(total, int) and len(rows) < total):
        page += 1; nxt = _call(env, server, tool, page=page, page_size=200, **kwargs)
        if not isinstance(nxt, dict) or not isinstance(nxt.get(rows_key), list) or not nxt[rows_key]:
            first["_pagination_incomplete"] = True; break
        rows.extend(nxt[rows_key]); first = nxt
        if len(rows) > 10000: first["_pagination_incomplete"] = True; break
    out = dict(first); out[rows_key] = rows; out["captured_complete"] = not out.get("_pagination_incomplete", False); return out

def _workspace_snapshot(env):
    fs = getattr(getattr(env, "workspace", None), "fs", None)
    if fs is None: return {}
    out = {}
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
        if depth <= 0: return
        for child in fs.list_dir(path): visit(f"{path.rstrip('/')}/{child}", depth-1)
    visit("/workspace", 4); return out

def capture_stage_snapshot(env: Any, stage_idx: int) -> dict[str, Any]:
    listings = ["lst_njr_0500","lst_njr_0511","lst_njr_0512","lst_njr_0513","lst_njr_0514","lst_njr_0515","lst_njr_0516","lst_njr_0518","lst_njr_0519","lst_njr_0599"]
    merchants = ["mer_njr_zhoumin","mer_njr_liqiang","mer_njr_zhenghao","mer_njr_sunlei"]
    return {
      "stage": stage_idx, "scenario_clock": scenario_clock(),
      "listing_platform": {"search": _call(env,"listing_platform","search_listings",city="Nanjing",district="Jiangbei New Area",page_size=200), "listings": {i:_call(env,"listing_platform","get_listing_detail",listing_id=i) for i in listings}, "market": {c:_call(env,"listing_platform","get_market_stats",area_or_community=c) for c in ["Mingfa Riverside New City","Top-of-the-Hill Street Xinyuan","Xuri Shangcheng","Hongyang Plaza Apartments"]}},
      "maps": {"transit": _call(env,"maps","get_transit",origin="Mingfa Riverside New City",destination="Software Avenue")},
      "review_platform": {"merchants": {i:_call(env,"review_platform","get_merchant",merchant_id=i) for i in merchants}},
      "banking": {"accounts": _call(env,"banking","list_accounts",user_id=USER_ID), "payees": _call(env,"banking","list_payees",user_id=USER_ID), "transactions": _call(env,"banking","list_transactions",account_id="acc_njr_chk",limit=500)},
      "email": {"inbox": _paged_call(env,"email","get_emails","emails",("id","email_id"),folder="INBOX"), "sent": _paged_call(env,"email","get_emails","emails",("id","email_id"),folder="Sent")},
      "notion": {"search": _call(env,"notion","API-post-search",query="",page_size=200)},
      "calendar": {"events": _call(env,"calendar","list_events",calendar_id="cal_njr_primary",max_results=500)},
      "workspace": _workspace_snapshot(env),
    }
