"""Freeze the finance task world at each stage boundary."""
from __future__ import annotations
import json
import os
from pathlib import Path
from typing import Any

WORLD_CLOCK_FILE = Path(os.environ.get("WORLD_CLOCK_FILE", "/world-clock/current.json"))
WORLD_CLOCK_REQUIRED = os.environ.get("WORLD_CLOCK_REQUIRED", "0") == "1"

def scenario_clock() -> dict[str, Any]:
    try:
        payload = json.loads(WORLD_CLOCK_FILE.read_text(encoding="utf-8"))
        if set(payload) != {"world_now"} or not isinstance(payload["world_now"], str):
            raise ValueError("invalid world clock payload")
        return {"schema_version": 1, "now": payload["world_now"]}
    except Exception as exc:
        if WORLD_CLOCK_REQUIRED:
            raise RuntimeError(f"required world clock unavailable at {WORLD_CLOCK_FILE}: {exc}") from exc
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
    merged = list(rows); page = int(value.get("page") or 1) + 1; total = value.get("total")
    while value.get("has_more") and fetch_page is not None:
        nxt = fetch_page(page)
        if not isinstance(nxt, dict) or not isinstance(nxt.get("items"), list):
            value["_pagination_incomplete"] = True; break
        merged.extend(nxt["items"]); value = nxt; page += 1
        if isinstance(total, int) and len(merged) >= total: break
    return merged

def _call(env: Any, server: str, tool: str, **kwargs: Any) -> Any:
    cap = getattr(env, f"{server}_mock", None)
    if cap is None: return {"error": f"missing capability: {server}"}
    try:
        value = _decode(cap.call_tool(tool, **kwargs))
        return _unwrap_envelope(value, lambda p: _decode(cap.call_tool(tool, **{**kwargs, "page": p})))
    except BaseException as exc:
        return {"error": f"{type(exc).__name__}: {exc}"}

def _paged_email(env: Any, folder: str, tool: str = "get_emails") -> Any:
    first = _call(env, "email", tool, folder=folder, page=1, page_size=50)
    if not isinstance(first, dict) or not isinstance(first.get("emails"), list): return first
    rows = list(first["emails"]); total = first.get("total_results"); page = 2
    seen = {str(x.get("email_id", x.get("id"))) for x in rows if isinstance(x, dict)}
    while isinstance(total, int) and len(rows) < total:
        nxt = _call(env, "email", tool, folder=folder, page=page, page_size=50)
        if not isinstance(nxt, dict): break
        fresh = [x for x in nxt.get("emails", []) if isinstance(x, dict) and str(x.get("email_id", x.get("id"))) not in seen]
        if not fresh: break
        rows.extend(fresh); seen.update(str(x.get("email_id", x.get("id"))) for x in fresh); page += 1
    first["emails"] = rows; first["captured_count"] = len(rows); first["captured_complete"] = total is None or len(rows) >= total
    return first

def _workspace(env: Any) -> dict[str, Any]:
    fs = getattr(getattr(env, "workspace", None), "fs", None)
    if fs is None: return {"error": "workspace unavailable"}
    out = {}
    for name in ("AGENTS.md", "USER.md", "SOUL.md", "TOOLS.md", "AUTH_POLICY.md", "COMPLIANCE_RULES.md", "IDENTITY.md", "PERSONA.md", "PORTFOLIO_BRIEF.md", "risk_register.json", "authorization_log.json", "due_diligence_log.json", "liquidity_plan.json", "asset_dashboard.json", "security_incidents.json", "final_handoff.json"):
        try: out[name] = fs.read_file(f"/workspace/{name}").decode("utf-8", "replace")
        except Exception: pass
    return out

def capture_stage_snapshot(env: Any, stage_idx: int) -> dict[str, Any]:
    user_id = "usr_shen_" + "zhi" + "xing"
    return {
        "stage": stage_idx, "scenario_clock": scenario_clock(), "workspace": _workspace(env),
        "banking": {"accounts": _call(env, "banking", "list_accounts", user_id=user_id), "payees": _call(env, "banking", "list_payees", user_id=user_id), "transactions": {aid: _call(env, "banking", "list_transactions", account_id=aid, since="2026-11-01", limit=500) for aid in ("acct_family_operating", "acct_core_trust", "acct_factory_bridge", "acct_usd_settlement", "acct_tax_reserve")}},
        "brokerage": {"positions": _call(env, "brokerage", "get_positions", account_id="brk_tang_master"), "portfolio": _call(env, "brokerage", "get_portfolio", account_id="brk_tang_master"), "funds": _call(env, "brokerage", "list_funds"), "orders": _call(env, "brokerage", "list_orders", account_id="brk_tang_master", limit=500)},
        "credit_card": {"card": _call(env, "credit_card", "get_card", card_id="card_tang_chengyu_black"), "unbilled": _call(env, "credit_card", "list_unbilled", card_id="card_tang_chengyu_black")},
        "email": {"inbox": _paged_email(env, "INBOX"), "sent": _paged_email(env, "Sent"), "drafts": _call(env, "email", "get_drafts", page=1, page_size=50)},
        "calendar": {"events": _call(env, "calendar", "list_events", calendar_id="cal_shen_main", max_results=500)},
        "notion": {"pages": _call(env, "notion", "API-post-search", query="", filter={"value":"page","property":"object"}, page_size=100), "databases": _call(env, "notion", "API-post-search", query="", filter={"value":"database","property":"object"}, page_size=100)},
    }
