"""Freeze the coastal sailing world through all task MCP services."""
from __future__ import annotations
import json, os
from datetime import datetime
from pathlib import Path
from typing import Any

WORLD_CLOCK = Path(os.environ.get("WORLD_CLOCK_FILE", "/world-clock/current.json"))
USER_ID = "usr_sailing_ops"
CALENDAR_ID = "cal_sailing_teamday"
BASELINE = {"AGENTS.md", "IDENTITY.md", "PERSONA.md", "SOUL.md", "TOOLS.md", "USER.md"}
# Merchants and deals the task's gates read back by id. The venue search is
# scoped to city='Shanghai' and the sail/photo vendors sit in 'Haiwan Marina',
# so their details are frozen explicitly instead of hoping a listing catches
# them.
REVIEW_MERCHANT_IDS = (
    "mer_harbor_cat_12", "mer_bay_breeze_12", "mer_cove_class_8",
    "mer_tide_table_dinner", "mer_lensharbor_photo",
)
REVIEW_DEAL_IDS = (
    "deal_harbor_cat_wave", "deal_bay_breeze_wave", "deal_cove_class_wave",
    "deal_tide_table_34", "deal_lensharbor_internal",
)

def _decode(value: Any) -> Any:
    if isinstance(value, str):
        try: return json.loads(value)
        except json.JSONDecodeError: return value
    return value

def _unwrap_envelope(value: Any, fetch_page=None) -> Any:
    if not isinstance(value, dict): return value
    rows = value.get("items")
    if not isinstance(rows, list) or ("total" not in value and "has_more" not in value): return value
    merged, current, page = list(rows), value, int(value.get("page") or 1)
    total = int(value["total"]) if isinstance(value.get("total"), (int, float)) else None
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
    except BaseException as exc:  # noqa: BLE001
        return {"error": f"{type(exc).__name__}: {exc}"}

def _paged_call(env: Any, server: str, tool: str, *, rows_key: str, id_keys: tuple[str, ...], **kwargs: Any) -> Any:
    first = _call(env, server, tool, page=1, page_size=50, **kwargs)
    if not isinstance(first, dict) or first.get("error"): return first
    rows = [r for r in (first.get(rows_key) or []) if isinstance(r, dict)]
    raw_total = first.get("total_results", first.get("total", len(rows)))
    total = int(raw_total) if isinstance(raw_total, (int, float)) else len(rows)
    def row_id(row): return next((str(row[k]) for k in id_keys if row.get(k) is not None), "")
    seen, page = {row_id(r) for r in rows}, 2
    while len(rows) < total:
        nxt = _call(env, server, tool, page=page, page_size=50, **kwargs)
        if not isinstance(nxt, dict) or nxt.get("error"): break
        fresh = [r for r in (nxt.get(rows_key) or []) if isinstance(r, dict) and row_id(r) not in seen]
        if not fresh: break
        rows.extend(fresh); seen.update(row_id(r) for r in fresh); page += 1
    first[rows_key], first["captured_count"], first["captured_complete"] = rows, len(rows), len(rows) >= total
    return first

def _email_folder(env, folder: str, details: bool) -> Any:
    listing = _paged_call(env, "email", "get_emails", rows_key="emails", id_keys=("email_id", "id"), folder=folder)
    if not details or not isinstance(listing, dict): return {"listing": listing, "details": []}
    out = []
    for row in listing.get("emails") or []:
        eid = (row.get("email_id") or row.get("id")) if isinstance(row, dict) else None
        if eid is None: continue
        detail, headers = _call(env, "email", "read_email", email_id=str(eid)), _call(env, "email", "get_email_headers", email_id=str(eid))
        if isinstance(detail, dict) and isinstance(headers, dict):
            for key in ("in_reply_to", "references", "references_header", "headers", "thread_id"):
                if headers.get(key) is not None: detail.setdefault(key, headers[key])
        out.append(detail)
    return {"listing": listing, "details": out}

def _workspace(env) -> dict[str, str]:
    fs = getattr(getattr(env, "workspace", None), "fs", None)
    if fs is None: return {}
    output, seen = {}, set()
    def visit(path, depth):
        if path in seen or len(output) >= 200: return
        seen.add(path); name = path.rsplit("/", 1)[-1]
        if name.startswith(".") or name in BASELINE: return
        if name.lower().endswith((".md", ".txt", ".json", ".csv")):
            try: raw = fs.read_file(path)
            except Exception: return
            text = raw.decode("utf-8", errors="replace") if isinstance(raw, bytes) else str(raw)
            if text.strip(): output[path] = text[:200000]
            return
        if depth <= 0: return
        try: children = fs.list_dir(path)
        except Exception: return
        for child in children: visit(f"{path.rstrip('/')}/{child}", depth - 1)
    visit("/workspace", 4); return output

def _clock() -> dict[str, str]:
    payload = json.loads(WORLD_CLOCK.read_text(encoding="utf-8"))
    if not isinstance(payload, dict) or set(payload) != {"world_now"}: raise RuntimeError("world clock must contain exactly world_now")
    value = payload.get("world_now")
    if not isinstance(value, str): raise RuntimeError("world_now must be a string")
    if datetime.fromisoformat(value.replace("Z", "+00:00")).tzinfo is None: raise RuntimeError("world_now must include a timezone")
    return {"world_now": value}

def _notion(env) -> dict[str, Any]:
    search = _call(env, "notion", "API-post-search", query="", page_size=100)
    rows = search.get("results", []) if isinstance(search, dict) else []
    dbs = {did: _call(env, "notion", "API-post-database-query", database_id=did, page_size=100) for did in ("db_sailing_roster", "db_sailing_gates")}
    blocks = {str(row["id"]): _call(env, "notion", "API-get-block-children", block_id=str(row["id"]), page_size=100) for row in rows if isinstance(row, dict) and row.get("id")}
    return {"search": search, "databases": dbs, "blocks": blocks}

def _detail_rows(env: Any, server: str, tool: str, id_key: str, ids: Any) -> list[dict[str, Any]]:
    """Freeze per-id tool details as a plain list of rows (no error blobs)."""
    out: list[dict[str, Any]] = []
    seen: set[str] = set()
    for raw in ids:
        wanted = str(raw)
        if not wanted or wanted in seen:
            continue
        seen.add(wanted)
        row = _call(env, server, tool, **{id_key: wanted})
        if isinstance(row, dict) and row and not row.get("error"):
            out.append(row)
    return out

def capture_stage_snapshot(env: Any, stage_idx: int) -> dict[str, Any]:
    reservations = _call(env, "review_platform", "list_reservations", user_id=USER_ID)
    reservation_rows = _unwrap_envelope(reservations) if isinstance(reservations, dict) else reservations
    if not isinstance(reservation_rows, list):
        reservation_rows = []
    merchant_ids = list(REVIEW_MERCHANT_IDS) + [
        row.get("merchant_id") for row in reservation_rows
        if isinstance(row, dict) and row.get("merchant_id")
    ]
    deal_ids = list(REVIEW_DEAL_IDS) + [
        row.get("deal_id") for row in reservation_rows
        if isinstance(row, dict) and row.get("deal_id")
    ]
    orders = _call(env, "ecommerce", "list_orders", user_id=USER_ID, limit=100)
    order_rows = _unwrap_envelope(orders) if isinstance(orders, dict) else orders
    if not isinstance(order_rows, list):
        order_rows = []
    products = _call(env, "ecommerce", "search_products", query="insurance", limit=100)
    product_rows = _unwrap_envelope(products) if isinstance(products, dict) else products
    if not isinstance(product_rows, list):
        product_rows = []
    return {
        "stage": int(stage_idx), "world_clock": _clock(), "workspace": _workspace(env),
        # INBOX needs bodies: the insurance certificate gate reads the mailed
        # "N adult boarding participants" count from read_email, so a
        # listing-only capture scores like the mail never arrived.
        "email": {"inbox": _email_folder(env, "INBOX", True), "sent": _email_folder(env, "Sent", True), "drafts": _paged_call(env, "email", "get_drafts", rows_key="drafts", id_keys=("draft_id", "id"))},
        "calendar": {"events": _call(env, "calendar", "list_events", calendar_id=CALENDAR_ID, max_results=500)},
        "notification_hub": {"notifications": _call(env, "notification_hub", "list_notifications", user_id=USER_ID, limit=500), "subscriptions": _call(env, "notification_hub", "list_subscriptions", user_id=USER_ID)},
        "notion": _notion(env),
        "maps": {"places": _call(env, "maps", "search_places", query="Haiwan Marina", limit=100), "directions": _call(env, "maps", "directions", origin="HQ", dest="Haiwan Marina"), "traffic": _call(env, "maps", "get_traffic_estimate", origin="HQ", dest="Haiwan Marina")},
        "review_platform": {
            "reservations": reservations,
            "merchants": _call(env, "review_platform", "search_merchants", category="venue", city="Shanghai", limit=100),
            "merchant_details": _detail_rows(env, "review_platform", "get_merchant", "merchant_id", merchant_ids),
            "deal_details": _detail_rows(env, "review_platform", "get_deal", "deal_id", deal_ids),
        },
        "ecommerce": {
            "orders": orders,
            "order_details": _detail_rows(env, "ecommerce", "get_order", "order_id", [row.get("order_id") for row in order_rows if isinstance(row, dict) and row.get("order_id")]),
            "products": products,
            "product_details": _detail_rows(env, "ecommerce", "get_product", "product_id", [row.get("product_id") for row in product_rows if isinstance(row, dict) and row.get("product_id")]),
        },
        "car_rental": {"bookings": _call(env, "car_rental", "list_bookings", user_id=USER_ID), "offers": _call(env, "car_rental", "search_vehicle_offers", pickup_city="Shanghai", return_city="Shanghai", pickup_at="2026-09-19T07:30:00+08:00", return_at="2026-09-19T21:30:00+08:00", seats=34, max_results=20)},
        "banking": {"transactions": _call(env, "banking", "list_transactions", account_id="acct_sailing_ops", limit=500), "payees": _call(env, "banking", "list_payees", user_id=USER_ID)},
        "weather": {"forecast": _call(env, "weather", "get_forecast_daily", geo="Haiwan Marina", days=14), "alerts": _call(env, "weather", "get_alerts", geo="Haiwan Marina")},
    }
