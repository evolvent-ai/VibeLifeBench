"""Freeze the flight attendant task MCP worlds at each stage boundary."""
from __future__ import annotations
import json, os
from pathlib import Path
from typing import Any

WORLD_CLOCK_FILE = Path(os.environ.get("WORLD_CLOCK_FILE", "/world-clock/current.json"))
USER_ID = "user_lin_rui"
CALENDAR_ID = "cal_linrui_primary"
BASELINE_WORKSPACE_NAMES = {"AGENTS.md","BUDGET_AUTH.md","HEALTH_BOUNDARIES.md","IDENTITY.md","PERSONA.md","PRIVACY_AUTH.md","SOUL.md","TOOLS.md","TRAINING_PRINCIPLES.md","USER.md"}
ALLOWED_WORKSPACE_SUFFIXES = (".md", ".txt", ".json", ".csv")

def scenario_clock() -> dict[str, Any]:
    try:
        payload = json.loads(WORLD_CLOCK_FILE.read_text(encoding="utf-8"))
        if not isinstance(payload, dict) or set(payload) != {"world_now"} or not isinstance(payload.get("world_now"), str): raise ValueError("invalid world clock payload")
        return {"schema_version": 1, "now": payload["world_now"]}
    except Exception as exc: raise RuntimeError(f"required world clock unavailable at {WORLD_CLOCK_FILE}: {exc}") from exc

def _decode(value: Any) -> Any:
    if isinstance(value, str):
        try: return json.loads(value)
        except json.JSONDecodeError: return value
    return value

def _unwrap_envelope(value: Any, fetch_page=None) -> Any:
    if not isinstance(value, dict): return value
    rows = value.get("items")
    if not isinstance(rows, list) or ("total" not in value and "has_more" not in value): return value
    merged = list(rows)
    if fetch_page is not None and value.get("has_more"):
        page = int(value.get("page") or 1); total = int(value["total"]) if isinstance(value.get("total"), (int,float)) else None; size = int(value.get("page_size") or 0) or max(len(merged),1); max_pages = ((total+size-1)//size+1) if total is not None else 1000; seen = {json.dumps(r, sort_keys=True, default=str) for r in merged}
        while value.get("has_more") and page < max_pages:
            page += 1; nxt = fetch_page(page)
            if not isinstance(nxt, dict): break
            fresh = []
            for row in nxt.get("items") or []:
                key = json.dumps(row, sort_keys=True, default=str)
                if key not in seen: fresh.append(row); seen.add(key)
            if not fresh: break
            merged.extend(fresh); value = nxt
        if total is not None and len(merged) < total: return {"items":merged,"_pagination_incomplete":True,"_captured":len(merged),"_total":total}
    return merged

def _call(env: Any, server: str, tool: str, **kwargs: Any) -> Any:
    cap = getattr(env, f"{server}_mock", None)
    if cap is None: return {"error": f"missing capability: {server}"}
    try:
        value = _decode(cap.call_tool(tool, **kwargs)); return _unwrap_envelope(value, lambda p: _decode(cap.call_tool(tool, **{**kwargs,"page":p})))
    except BaseException as exc: return {"error": f"{type(exc).__name__}: {exc}"}

def _paged_call(env: Any, server: str, tool: str, *, rows_key: str, id_keys: tuple[str,...], **kwargs: Any) -> Any:
    first = _call(env,server,tool,page=1,page_size=200,**kwargs)
    if not isinstance(first,dict): return first
    rows=[r for r in (first.get(rows_key) or []) if isinstance(r,dict)]; raw=first.get("total_results",first.get("total")); total=int(raw) if isinstance(raw,(int,float)) else None; size=int(first.get("page_size") or 0) or max(len(rows),1); seen={str(next((r.get(k) for k in id_keys if r.get(k) is not None),"")) for r in rows}; page=2
    while total is not None and len(rows)<total and page<=((total+size-1)//size+1):
        nxt=_call(env,server,tool,page=page,page_size=size,**kwargs)
        if not isinstance(nxt,dict): break
        fresh=[r for r in (nxt.get(rows_key) or []) if isinstance(r,dict) and str(next((r.get(k) for k in id_keys if r.get(k) is not None),"")) not in seen]
        if not fresh: break
        rows.extend(fresh); seen.update(str(next((r.get(k) for k in id_keys if r.get(k) is not None),"")) for r in fresh); page+=1
    first[rows_key]=rows; first["captured_count"]=len(rows)
    if total is not None: first["captured_complete"]=len(rows)>=total
    return first

def _email_snapshot(env: Any, folder: str) -> dict[str, Any]:
    # Bodies ride along in the listing rows: per-email read_email round-trips
    # were timeout-prone at INBOX scale and marked mail as read as a capture
    # side effect. The listing row keys stay identical, plus body_text/body_html.
    listing=_paged_call(env,"email","get_emails",rows_key="emails",id_keys=("email_id","id"),folder=folder,include_body=True)
    return {"listing":listing,"details":[]}

def _orders_snapshot(env: Any) -> Any:
    # list_orders returns header rows without line items; merge each get_order
    # detail (items/status_history/refunds) into its header row so order-level
    # checks can read items from the frozen evidence. _call already flattens
    # the {"items": [...], "total": ...} envelope into a bare row list, so
    # handle both that list and a still-envelope dict.
    listing=_call(env,"ecommerce","list_orders",user_id=USER_ID,limit=800)
    rows=listing.get("items") if isinstance(listing,dict) else listing
    if not isinstance(rows,list): return listing
    for row in rows:
        order_id=row.get("order_id") if isinstance(row,dict) else None
        if not order_id: continue
        detail=_call(env,"ecommerce","get_order",order_id=str(order_id))
        if isinstance(detail,dict) and "error" not in detail: row.update(detail)
    return listing

def _workspace_snapshot(env: Any) -> dict[str,str]:
    fs=getattr(getattr(env,"workspace",None),"fs",None)
    if fs is None:return {}
    out={}; seen=set()
    def visit(path,depth):
        if path in seen or len(out)>=200:return
        seen.add(path); name=path.rsplit("/",1)[-1]
        if name in BASELINE_WORKSPACE_NAMES or name.startswith("."):return
        if name.lower().endswith(ALLOWED_WORKSPACE_SUFFIXES):
            try: raw=fs.read_file(path)
            except Exception: raw=None
            if raw is not None and str(raw).strip(): out[path]=raw.decode("utf-8","replace") if isinstance(raw,bytes) else str(raw)
            return
        if depth<=0:return
        for child in fs.list_dir(path): visit(f"{path.rstrip('/')}/{child}",depth-1)
    visit("/workspace",4); return out

def _notion_snapshot(env: Any) -> dict[str,Any]:
    pages=_call(env,"notion","API-post-search",query="",filter={"value":"page","property":"object"},page_size=100); databases=_call(env,"notion","API-post-search",query="",filter={"value":"database","property":"object"},page_size=100)
    def ids(data): return [str(x["id"]) for x in (data.get("results") or []) if isinstance(x,dict) and x.get("id")] if isinstance(data,dict) else []
    page_blocks={i:_call(env,"notion","API-get-block-children",block_id=i,page_size=100) for i in ids(pages)}; database_rows={}; row_children={}
    for i in ids(databases):
        rows=_call(env,"notion","API-post-database-query",database_id=i,page_size=100); database_rows[i]=rows
        for rid in ids(rows): row_children[rid]=_call(env,"notion","API-get-block-children",block_id=rid,page_size=100)
    return {"pages":pages,"databases":databases,"page_blocks":page_blocks,"database_rows":database_rows,"row_children":row_children}

def capture_stage_snapshot(env: Any, stage_idx: int) -> dict[str,Any]:
    return {"stage":stage_idx,"scenario_clock":scenario_clock(),"calendar":{"events":_call(env,"calendar","list_events",calendar_id=CALENDAR_ID,max_results=800),"calendars":_call(env,"calendar","list_calendars")},"health_tracker":{"metrics":{t:_call(env,"health_tracker","get_metrics",user_id=USER_ID,type=t,limit=800) for t in ("steps","sleep_minutes","heart_rate","score","weight")},"workouts":_call(env,"health_tracker","list_workouts",user_id=USER_ID,limit=800),"goals":_call(env,"health_tracker","get_goals",user_id=USER_ID),"alerts":_call(env,"health_tracker","list_health_alerts",user_id=USER_ID)},"weather":{"daily":_call(env,"weather","get_forecast_daily",geo="Shanghai",days=60),"hourly":_call(env,"weather","get_forecast_hourly",geo="Shanghai",hours=500),"alerts":_call(env,"weather","get_alerts",geo="Shanghai"),"aqi":_call(env,"weather","get_aqi",geo="Shanghai")},"email":{"inbox":_email_snapshot(env,"INBOX"),"sent":_email_snapshot(env,"Sent"),"drafts":_paged_call(env,"email","get_drafts",rows_key="drafts",id_keys=("draft_id","id"))},"ecommerce":{"products":_call(env,"ecommerce","search_products",query="",limit=800),"orders":_orders_snapshot(env)},"notion":_notion_snapshot(env),"workspace":_workspace_snapshot(env)}
