"""Capture the stroller task's seven service backends at each stage boundary."""
from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

SCENARIO_CLOCK_PATH = Path(os.environ.get("SCENARIO_CLOCK_PATH", "/scenario-clock/current.json"))
SCENARIO_CLOCK_REQUIRED = os.environ.get("SCENARIO_CLOCK_REQUIRED", "0") == "1"
USER_ID = "usr_yan_ting"
ORDER_IDS = ("ord_strr_0001", "ord_strr_0002")
PRODUCT_IDS = ("prod_strr_main", "bnd_strr_a3", "bnd_strr_b2", "bnd_strr_c3")
LISTING_IDS = ("lst_strr_0001",)
CARD_ID = "card_strr_01"


def scenario_clock() -> dict[str, Any]:
    try:
        payload = json.loads(SCENARIO_CLOCK_PATH.read_text(encoding="utf-8"))
        value = payload.get("world_now") if isinstance(payload, dict) else None
        if not isinstance(value, str) or not value:
            raise ValueError("invalid scenario clock payload")
        return {"schema_version": 1, "step": payload.get("step", "unknown"), "now": value}
    except Exception as exc:
        if SCENARIO_CLOCK_REQUIRED:
            raise RuntimeError(f"required scenario clock unavailable: {exc}") from exc
        return {"schema_version": 1, "step": "unknown", "now": ""}


def _decode(value: Any) -> Any:
    if isinstance(value, str):
        try:
            return json.loads(value)
        except json.JSONDecodeError:
            return value
    return value


def _unwrap_envelope(value: Any, fetch_page: Any = None) -> Any:
    """Flatten the current paginated server envelope into the legacy row list."""
    if not isinstance(value, dict):
        return value
    rows = value.get("items")
    if not isinstance(rows, list):
        return value
    if "total" not in value and "has_more" not in value:
        return value
    merged = list(rows)
    if fetch_page is not None and value.get("has_more"):
        page = int(value.get("page") or 1)
        total = value.get("total")
        total = int(total) if isinstance(total, (int, float)) else None
        size = int(value.get("page_size") or 0) or max(len(merged), 1)
        max_pages = ((total + size - 1) // size + 1) if total else 1000
        seen = {json.dumps(row, sort_keys=True, default=str) for row in merged}
        while value.get("has_more") and page < max_pages:
            page += 1
            nxt = fetch_page(page)
            if not isinstance(nxt, dict) or not isinstance(nxt.get("items"), list):
                break
            fresh = []
            for row in nxt["items"]:
                marker = json.dumps(row, sort_keys=True, default=str)
                if marker not in seen:
                    seen.add(marker)
                    fresh.append(row)
            if not fresh:
                break
            merged.extend(fresh)
            value = nxt
        if total is not None and len(merged) < total:
            return {"items": merged, "_pagination_incomplete": True,
                    "_captured": len(merged), "_total": total}
    return merged


def _call(env: Any, server: str, tool: str, **kwargs: Any) -> Any:
    cap = getattr(env, f"{server}_mock", None)
    if cap is None:
        return {"error": f"missing capability: {server}"}
    try:
        value = _decode(cap.call_tool(tool, **kwargs))
        return _unwrap_envelope(
            value,
            lambda page: _decode(cap.call_tool(tool, **{**kwargs, "page": page})),
        )
    except BaseException as exc:  # noqa: BLE001 - preserve capture errors
        return {"error": f"{type(exc).__name__}: {exc}"}


def _workspace_snapshot(env: Any) -> dict[str, str]:
    fs = getattr(getattr(env, "workspace", None), "fs", None)
    if fs is None:
        return {}
    baseline = {"AGENTS.md", "IDENTITY.md", "PERSONA.md", "SOUL.md", "TOOLS.md", "USER.md"}
    out: dict[str, str] = {}
    try:
        names = fs.list_dir("/workspace")
    except Exception:
        return out
    for name in names:
        if name in baseline or name.startswith(".") or not name.lower().endswith((".md", ".txt", ".json", ".csv")):
            continue
        path = f"/workspace/{name}"
        try:
            raw = fs.read_file(path)
        except Exception:
            continue
        text = raw.decode("utf-8", errors="replace") if isinstance(raw, bytes) else str(raw)
        if text.strip():
            out[path] = text[:200000]
    return out


def capture_stage_snapshot(env: Any, stage_idx: int) -> dict[str, Any]:
    """Return stable, read-only projections consumed by the Harbor rubrics."""
    orders = [_call(env, "ecommerce", "get_order", order_id=order_id) for order_id in ORDER_IDS]
    products = [_call(env, "ecommerce", "get_product", product_id=product_id) for product_id in PRODUCT_IDS]
    return {
        "stage": stage_idx,
        "scenario_clock": scenario_clock(),
        "ecommerce": {
            "orders": orders,
            "products": products,
            "cart": _call(env, "ecommerce", "get_cart", user_id=USER_ID),
        },
        "delivery_logistics": {
            "shipments": _call(env, "delivery_logistics", "list_shipments", user_id=USER_ID, limit=100),
        },
        "credit_card": {
            "cards": [_call(env, "credit_card", "get_card", card_id=CARD_ID)],
            "disputes": _call(env, "credit_card", "list_disputes", card_id=CARD_ID),
            "unbilled_transactions": _call(env, "credit_card", "list_unbilled", card_id=CARD_ID),
        },
        "email": {
            "inbox": _call(env, "email", "get_emails", folder="INBOX", page=1, page_size=200),
            "sent": _call(env, "email", "get_emails", folder="Sent", page=1, page_size=200),
            "drafts": _call(env, "email", "get_drafts", page=1, page_size=200),
        },
        "calendar": {
            "events": _call(env, "calendar", "list_events", max_results=500),
        },
        "notification_hub": {
            "notifications": _call(env, "notification_hub", "list_notifications", user_id=USER_ID, limit=500),
            "subscriptions": _call(env, "notification_hub", "list_subscriptions", user_id=USER_ID),
        },
        "listing_platform": {
            "listings": [_call(env, "listing_platform", "get_listing", listing_id=listing_id) for listing_id in LISTING_IDS],
        },
        "workspace": _workspace_snapshot(env),
    }
