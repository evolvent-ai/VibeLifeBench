"""Trusted, fail-closed snapshots for the litigation workflow."""
from __future__ import annotations
import json, os
from datetime import datetime
from pathlib import Path
from typing import Any

SCENARIO_CLOCK_PATH = Path(os.environ.get("WORLD_CLOCK_FILE", "/world-clock/current.json"))
SCENARIO_CLOCK_REQUIRED = os.environ.get("WORLD_CLOCK_REQUIRED", "0") == "1"
USER_ID = "han_yushan"
CALENDAR_ID = "cal_han_primary"

def scenario_clock() -> dict[str, Any]:
    try:
        payload=json.loads(SCENARIO_CLOCK_PATH.read_text(encoding="utf-8"))
        now=str(payload["now"]); datetime.fromisoformat(now.replace("Z","+00:00"))
        step=str(payload["step"])
        if not step: raise ValueError("invalid clock step")
        return {"schema_version":1,"step":step,"now":now}
    except Exception as exc:
        if SCENARIO_CLOCK_REQUIRED: raise RuntimeError(f"required world clock unavailable: {exc}") from exc
        return {"schema_version":1,"step":"unknown","now":""}

def _decode(value: Any) -> Any:
    if isinstance(value,str):
        try:return json.loads(value)
        except json.JSONDecodeError:return value
    return value

def _unwrap_envelope(value: Any, fetch_page=None) -> Any:
    if not isinstance(value,dict): return value
    rows=value.get("items")
    if not isinstance(rows,list) or ("total" not in value and "has_more" not in value): return value
    merged=list(rows); total=value.get("total"); page=int(value.get("page") or 1); current=value
    while fetch_page is not None and current.get("has_more") and (not isinstance(total,int) or len(merged)<total):
        page += 1; nxt=fetch_page(page)
        if not isinstance(nxt,dict) or not isinstance(nxt.get("items"),list) or not nxt["items"]:
            current["_pagination_incomplete"]=True; break
        merged.extend(nxt["items"]); current=nxt
    if isinstance(total,int) and len(merged)<total: current["_pagination_incomplete"]=True
    return merged

def _call(env: Any, server: str, tool: str, **kwargs: Any) -> Any:
    cap=getattr(env,f"{server}_mock",None)
    if cap is None:return {"error":f"missing capability: {server}"}
    try:
        raw=_decode(cap.call_tool(tool,**kwargs))
        return _unwrap_envelope(raw,lambda p:_decode(cap.call_tool(tool,**{**kwargs,"page":p})))
    except BaseException as exc:return {"error":f"{type(exc).__name__}: {exc}"}

def _paged_call(env: Any, server: str, tool: str, rows_key: str, id_keys: tuple[str,...], **kwargs: Any) -> Any:
    first=_call(env,server,tool,page=1,page_size=200,**kwargs)
    if not isinstance(first,dict) or not isinstance(first.get(rows_key),list):return first
    rows=list(first[rows_key]); total=first.get("total_results",first.get("total")); seen={str(next((r.get(k) for k in id_keys if isinstance(r,dict) and r.get(k) is not None),"")) for r in rows}; page=2
    while isinstance(total,(int,float)) and len(rows)<int(total) and page<100:
        nxt=_call(env,server,tool,page=page,page_size=max(len(rows),1),**kwargs)
        if not isinstance(nxt,dict) or not isinstance(nxt.get(rows_key),list):first["_pagination_incomplete"]=True;break
        fresh=[r for r in nxt[rows_key] if str(next((r.get(k) for k in id_keys if isinstance(r,dict) and r.get(k) is not None),"")) not in seen]
        if not fresh:first["_pagination_incomplete"]=True;break
        rows.extend(fresh);seen.update(str(next((r.get(k) for k in id_keys if isinstance(r,dict) and r.get(k) is not None),"")) for r in fresh);page+=1
    first[rows_key]=rows;first["captured_count"]=len(rows);first["captured_complete"]=not isinstance(total,(int,float)) or len(rows)>=int(total);return first

def _workspace_snapshot(env: Any) -> dict[str,str]:
    fs=getattr(getattr(env,"workspace",None),"fs",None)
    if fs is None:return {}
    out={}
    try:
        for name in fs.list_dir("/workspace"):
            if name.endswith((".json",".md",".txt",".csv")):
                path=f"/workspace/{name}"
                try:out[path]=fs.read_file(path).decode("utf-8",errors="replace")[:200000]
                except Exception:pass
    except Exception:pass
    return out

def capture_stage_snapshot(env: Any, stage_idx: int) -> dict[str,Any]:
    return {
      "stage":stage_idx,"scenario_clock":scenario_clock(),"workspace":_workspace_snapshot(env),
      "calendar":{"calendars":_call(env,"calendar","list_calendars",user_id=USER_ID),"events":_call(env,"calendar","list_events",calendar_id=CALENDAR_ID,max_results=500)},
      "email":{"inbox":_paged_call(env,"email","get_emails","emails",("email_id","id"),folder="INBOX"),"sent":_paged_call(env,"email","get_emails","emails",("email_id","id"),folder="Sent"),"drafts":_paged_call(env,"email","get_drafts","drafts",("draft_id","id"))},
      "legal_search":{"saved":_call(env,"legal_search","list_saved",user_id=USER_ID),"cases":_call(env,"legal_search","search_cases",query="water leak",limit=100),"statutes":_call(env,"legal_search","search_statutes",query="property damage",limit=100)},
      "notion":{"pages":_call(env,"notion","API-post-search",query="",filter={"value":"page"},page_size=100)},
      "review_platform":{"merchants":_call(env,"review_platform","search_merchants",query="",category="home_service",city="Shanghai",page=1,page_size=100),"reviews":_call(env,"review_platform","list_reviews",merchant_id="mer_home_haize_025",limit=100),"saved":_call(env,"review_platform","list_saved_merchants",user_id=USER_ID),"reservations":_call(env,"review_platform","list_reservations",user_id=USER_ID)},
    }
