"""Capture the old-home rental world into immutable Harbor evidence."""
from __future__ import annotations

import json
import os
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Any

WORLD_CLOCK_FILE = Path(os.environ.get("WORLD_CLOCK_FILE", "/scenario-clock/current.json"))
USER_ID = "usr_zhanglan"
CALENDAR_ID = "cal_zl_rental_reno"
LISTING_ID = "lst_rental_profile_hj603"
LISTING_IDS = (LISTING_ID,)
DB_PATHS = {
    "banking": Path("/banking-env/runtime.db"),
    "listing_platform": Path("/listing-platform-env/runtime.db"),
    "calendar": Path("/calendar-env/runtime.db"),
    "notification_hub": Path("/notification-hub-env/runtime.db"),
    "delivery_logistics": Path("/delivery-logistics-env/runtime.db"),
    "ecommerce": Path("/ecommerce-env/runtime.db"),
    "email": Path("/email-env/runtime.db"),
    "legal_search": Path("/legal-search-env/runtime.db"),
}
BASELINE_WORKSPACE_NAMES = {
    "AGENTS.md",
    "IDENTITY.md",
    "PERSONA.md",
    "SOUL.md",
    "TOOLS.md",
    "USER.md",
    "ARTIFACT_CONTRACT.md",
    "RENOVATION_RENTAL_BRIEF.md",
}


def _connect(server: str) -> sqlite3.Connection:
    path = DB_PATHS[server]
    if not path.is_file():
        raise RuntimeError(f"snapshot database is unavailable: {path}")
    conn = sqlite3.connect(
        f"file:{path}?mode=ro",
        uri=True,
        timeout=15.0,
        isolation_level=None,
    )
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA query_only = ON")
    conn.execute("PRAGMA busy_timeout = 15000")
    return conn


def _loads(value: Any, default: Any = None) -> Any:
    if value is None or value == "":
        return default
    try:
        return json.loads(value)
    except (TypeError, ValueError):
        return value


def _listing_summary(row: sqlite3.Row) -> dict[str, Any]:
    return {
        "listing_id": row["listing_id"],
        "category": row["category"],
        "title": row["title"],
        "city": row["city"],
        "district": row["district"],
        "community": row["community"],
        "price_minor": int(row["price_minor"]),
        "area_sqm": row["area_sqm"],
        "rooms": row["rooms"],
        "metro": row["metro"],
        "agent_id": row["agent_id"],
        "status": row["status"],
        "listed_at": row["listed_at"],
    }


def _listing_detail(conn: sqlite3.Connection, listing_id: str) -> dict[str, Any]:
    row = conn.execute(
        "SELECT * FROM listings WHERE listing_id = ?", (listing_id,)
    ).fetchone()
    if row is None:
        return {"code": "LISTING_NOT_FOUND", "error": f"listing not found: {listing_id}"}
    detail = _listing_summary(row)
    detail.update(
        {
            "attrs": _loads(row["attrs_json"], {}),
            "photos": _loads(row["photos_json"], []),
            "description": row["description"],
            "owner_user_id": row["owner_user_id"],
        }
    )
    agent = None
    if row["agent_id"]:
        agent_row = conn.execute(
            "SELECT * FROM agents WHERE agent_id = ?", (row["agent_id"],)
        ).fetchone()
        if agent_row is not None:
            agent = {
                "agent_id": agent_row["agent_id"],
                "name": agent_row["name"],
                "agency": agent_row["agency"],
                "phone": agent_row["phone"],
                "rating": agent_row["rating"],
                "deals_count": int(agent_row["deals_count"]),
                "service_area": agent_row["service_area"],
            }
    detail["agent"] = agent
    return detail


def _listing_snapshot() -> dict[str, Any]:
    conn = _connect("listing_platform")
    try:
        saved_rows = conn.execute(
            """
            SELECT l.*, s.saved_at AS _saved_at
            FROM saved_listings s
            JOIN listings l ON l.listing_id = s.listing_id
            WHERE s.user_id = ?
            ORDER BY s.saved_at ASC, l.listing_id ASC
            """,
            (USER_ID,),
        ).fetchall()
        saved = []
        for row in saved_rows:
            item = _listing_summary(row)
            item["saved_at"] = row["_saved_at"]
            saved.append(item)
        viewing_rows = conn.execute(
            """
            SELECT v.viewing_id, v.listing_id, v.agent_id, v.scheduled_at,
                   v.status, v.created_at, l.title AS listing_title,
                   l.community AS listing_community
            FROM viewings v
            LEFT JOIN listings l ON l.listing_id = v.listing_id
            WHERE v.user_id = ?
            ORDER BY v.scheduled_at ASC, v.viewing_id ASC
            """,
            (USER_ID,),
        ).fetchall()
        viewings = [
            {
                "viewing_id": row["viewing_id"],
                "listing_id": row["listing_id"],
                "listing_title": row["listing_title"],
                "listing_community": row["listing_community"],
                "agent_id": row["agent_id"],
                "scheduled_at": row["scheduled_at"],
                "status": row["status"],
                "created_at": row["created_at"],
            }
            for row in viewing_rows
        ]
        listing_rows = conn.execute("SELECT listing_id FROM listings ORDER BY listing_id ASC").fetchall()
        listings = {
            str(row["listing_id"]): _listing_detail(conn, str(row["listing_id"]))
            for row in listing_rows
        }
        return {"saved": saved, "viewings": viewings, "listings": listings}
    finally:
        conn.close()


def _calendar_snapshot() -> dict[str, Any]:
    conn = _connect("calendar")
    try:
        calendar_rows = conn.execute(
            """
            SELECT calendar_id, user_id, name, color, timezone, is_primary, created_at
            FROM calendars WHERE user_id = ?
            ORDER BY is_primary DESC, created_at ASC, calendar_id ASC
            """,
            (USER_ID,),
        ).fetchall()
        calendars = [
            {
                "calendar_id": row["calendar_id"],
                "user_id": row["user_id"],
                "name": row["name"],
                "color": row["color"],
                "timezone": row["timezone"],
                "is_primary": bool(int(row["is_primary"])),
                "created_at": row["created_at"],
            }
            for row in calendar_rows
        ]
        event_rows = conn.execute(
            """
            SELECT * FROM events WHERE calendar_id = ?
            ORDER BY start_dt ASC, event_id ASC LIMIT 500
            """,
            (CALENDAR_ID,),
        ).fetchall()
        events = []
        for row in event_rows:
            event_id = row["event_id"]
            attendees = [
                {
                    "email": item["email"],
                    "name": item["name"],
                    "response_status": item["response_status"],
                }
                for item in conn.execute(
                    """
                    SELECT email, name, response_status FROM attendees
                    WHERE event_id = ? ORDER BY id ASC
                    """,
                    (event_id,),
                ).fetchall()
            ]
            reminders = [
                {"method": item["method"], "minutes_before": int(item["minutes_before"])}
                for item in conn.execute(
                    """
                    SELECT method, minutes_before FROM reminders
                    WHERE event_id = ? ORDER BY minutes_before DESC, id ASC
                    """,
                    (event_id,),
                ).fetchall()
            ]
            events.append(
                {
                    "event_id": event_id,
                    "calendar_id": row["calendar_id"],
                    "summary": row["summary"],
                    "description": row["description"],
                    "location": row["location"],
                    "start": {"dateTime": row["start_dt"]},
                    "end": {"dateTime": row["end_dt"]},
                    "all_day": bool(int(row["all_day"])),
                    "status": row["status"],
                    "created_at": row["created_at"],
                    "updated_at": row["updated_at"],
                    "recurrence_rule": row["recurrence_rule"],
                    "parent_event_id": row["parent_event_id"],
                    "attendees": attendees,
                    "reminders": reminders,
                }
            )
        return {"calendars": calendars, "events": events}
    finally:
        conn.close()


def _notification_snapshot() -> dict[str, Any]:
    conn = _connect("notification_hub")
    try:
        subscription_rows = conn.execute(
            """
            SELECT * FROM subscriptions
            WHERE user_id = ? AND status != 'deleted'
            ORDER BY created_at ASC, subscription_id ASC
            """,
            (USER_ID,),
        ).fetchall()
        subscriptions = [
            {
                "subscription_id": row["subscription_id"],
                "user_id": row["user_id"],
                "source": row["source"],
                "type": row["type"],
                "target": row["target"],
                "condition": _loads(row["condition_json"]),
                "status": row["status"],
                "created_at": row["created_at"],
                "updated_at": row["updated_at"],
            }
            for row in subscription_rows
        ]
        alert_rows = conn.execute(
            """
            SELECT * FROM price_alerts WHERE user_id = ?
            ORDER BY created_at ASC, alert_id ASC
            """,
            (USER_ID,),
        ).fetchall()
        price_alerts = [
            {
                "alert_id": row["alert_id"],
                "user_id": row["user_id"],
                "item_ref": row["item_ref"],
                "target_price_minor": int(row["target_price_minor"]),
                "currency": row["currency"],
                "status": row["status"],
                "created_at": row["created_at"],
            }
            for row in alert_rows
        ]
        notification_rows = conn.execute(
            """
            SELECT * FROM notifications WHERE user_id = ?
            ORDER BY created_at DESC, notification_id DESC LIMIT 500
            """,
            (USER_ID,),
        ).fetchall()
        notifications = [
            {
                "notification_id": row["notification_id"],
                "user_id": row["user_id"],
                "source": row["source"],
                "type": row["type"],
                "subscription_id": row["subscription_id"],
                "title": row["title"],
                "body": row["body"],
                "payload": _loads(row["payload_json"]),
                "created_at": row["created_at"],
                "read": bool(int(row["read"])),
            }
            for row in notification_rows
        ]
        return {
            "subscriptions": subscriptions,
            "price_alerts": price_alerts,
            "notifications": notifications,
        }
    finally:
        conn.close()


def _world_clock() -> dict[str, Any]:
    try:
        payload = json.loads(WORLD_CLOCK_FILE.read_text(encoding="utf-8"))
        if set(payload) != {"schema_version", "step", "world_now"}:
            raise ValueError("invalid world clock keys")
        if payload.get("schema_version") != 1:
            raise ValueError("invalid world clock schema version")
        if not isinstance(payload.get("step"), str) or not isinstance(payload.get("world_now"), str):
            raise ValueError("invalid world clock payload")
        parsed = datetime.fromisoformat(payload["world_now"].replace("Z", "+00:00"))
        if parsed.tzinfo is None or parsed.utcoffset() is None:
            raise ValueError("world clock must include an offset")
        return {"schema_version": 1, "step": payload["step"], "world_now": parsed.isoformat()}
    except Exception as exc:
        raise RuntimeError(
            f"required world clock unavailable at {WORLD_CLOCK_FILE}: {exc}"
        ) from exc


def _decode(value: Any) -> Any:
    if isinstance(value, bytes):
        value = value.decode("utf-8", errors="replace")
    if isinstance(value, str):
        try:
            return json.loads(value)
        except (TypeError, ValueError):
            return value
    return value


def _rows(value: Any, *keys: str) -> list[dict[str, Any]]:
    if isinstance(value, list):
        return [row for row in value if isinstance(row, dict)]
    if isinstance(value, dict):
        for key in keys:
            candidate = value.get(key)
            if isinstance(candidate, list):
                return [row for row in candidate if isinstance(row, dict)]
    return []


def _live_call(env: Any, server: str, tool: str, **kwargs: Any) -> Any:
    """Read one live capability and fail closed on a server-side error."""
    capability = getattr(env, f"{server}_mock", None)
    if capability is None:
        raise RuntimeError(f"missing capture capability: {server}")
    try:
        value = _decode(capability.call_tool(tool, **kwargs))
    except Exception as exc:  # noqa: BLE001 - capture must not publish partial state
        raise RuntimeError(f"{server}.{tool} failed: {type(exc).__name__}: {exc}") from exc
    if isinstance(value, dict) and (
        value.get("error") not in (None, "")
        or value.get("isError") is True
        or value.get("is_error") is True
        or value.get("ok") is False
    ):
        raise RuntimeError(f"{server}.{tool} returned an error envelope: {value}")
    return value


def _workspace_snapshot(workspace_root: Path | str) -> dict[str, str]:
    """Capture every non-baseline text artifact, including nested files."""
    root = Path(workspace_root)
    if not root.is_dir() or root.is_symlink():
        return {}
    captured: dict[str, str] = {}
    allowed = {".md", ".txt", ".json", ".csv"}
    for candidate in sorted(root.rglob("*")):
        if not candidate.is_file() or candidate.is_symlink():
            continue
        if any(part.startswith(".") for part in candidate.relative_to(root).parts):
            continue
        if candidate.name in BASELINE_WORKSPACE_NAMES or candidate.suffix.lower() not in allowed:
            continue
        text = candidate.read_text(encoding="utf-8", errors="replace")
        if text.strip():
            relative = candidate.relative_to(root).as_posix()
            captured[f"/workspace/{relative}"] = text[:200000]
    return captured


def _workspace_snapshot_live(env: Any) -> dict[str, str]:
    fs = getattr(getattr(env, "workspace", None), "fs", None)
    if fs is None:
        raise RuntimeError("live workspace capability is unavailable")
    captured: dict[str, str] = {}
    allowed = {".md", ".txt", ".json", ".csv"}

    def visit(path: str, depth: int) -> None:
        if depth < 0 or len(captured) >= 200:
            return
        name = path.rsplit("/", 1)[-1]
        if name.startswith(".") or name in BASELINE_WORKSPACE_NAMES:
            return
        suffix = Path(name).suffix.lower()
        if suffix in allowed:
            try:
                raw = fs.read_file(path)
            except FileNotFoundError:
                return
            text = raw.decode("utf-8", errors="replace") if isinstance(raw, bytes) else str(raw)
            if text.strip():
                captured[path] = text[:200000]
            return
        for child in fs.list_dir(path):
            visit(f"{path.rstrip('/')}/{child}", depth - 1)

    visit("/workspace", 4)
    return captured


def _connect_server(server: str) -> sqlite3.Connection:
    path = DB_PATHS[server]
    if not path.is_file():
        raise RuntimeError(f"snapshot database is unavailable: {path}")
    conn = sqlite3.connect(f"file:{path}?mode=ro", uri=True, timeout=15.0, isolation_level=None)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA query_only = ON")
    conn.execute("PRAGMA busy_timeout = 15000")
    return conn


def _table(conn: sqlite3.Connection, name: str) -> list[dict[str, Any]]:
    return [dict(row) for row in conn.execute(f'SELECT * FROM "{name}"').fetchall()]


def _banking_snapshot() -> dict[str, Any]:
    conn = _connect_server("banking")
    try:
        account_rows = _table(conn, "accounts")
        accounts = {
            str(row["account_id"]): {
                **row,
                "balance_minor": int(row.get("balance_minor") or 0),
                "frozen": bool(int(row.get("frozen") or 0)),
            }
            for row in account_rows
        }
        # Rubrics query the renovation account through list_transactions; keep
        # that projection account-scoped so an unrelated household payment with
        # a similar redacted counterparty cannot be mistaken for project spend.
        transactions = [
            row for row in _table(conn, "transactions")
            if row.get("account_id") == "acct_zl_renovation"
        ]
        for row in transactions:
            row["amount_minor"] = int(row.get("amount_minor") or 0)
            row["balance_after_minor"] = int(row.get("balance_after_minor") or 0)
        return {"accounts": accounts, "transactions": transactions, "payees": _table(conn, "payees")}
    finally:
        conn.close()


def _delivery_snapshot() -> dict[str, Any]:
    conn = _connect_server("delivery_logistics")
    try:
        shipments: dict[str, dict[str, Any]] = {}
        for row in _table(conn, "shipments"):
            shipment_id = str(row["shipment_id"])
            def loads(key: str, default: Any) -> Any:
                try:
                    return json.loads(row.get(key) or "")
                except (TypeError, ValueError):
                    return default
            events = [event for event in _table(conn, "shipment_events") if event.get("shipment_id") == shipment_id]
            subscriptions = [
                {**sub, "active": bool(int(sub.get("active") or 0))}
                for sub in _table(conn, "status_subscriptions")
                if sub.get("shipment_id") == shipment_id
            ]
            shipments[shipment_id] = {
                "shipment_id": shipment_id,
                "user_id": row["user_id"],
                "tracking_no": row["tracking_no"],
                "carrier": row["carrier"],
                "service_level": row["service_level"],
                "status": row["status"],
                "sender": loads("sender_json", {}),
                "recipient": loads("recipient_json", {}),
                "weight_kg": float(row["weight_kg"]),
                "dimensions": loads("dimensions_json", {}),
                "declared_value_minor": int(row["declared_value_minor"]),
                "fee_minor": int(row["fee_minor"]),
                "created_at": row["created_at"],
                "eta_date": row["eta_date"],
                "scheduled_pickup_at": row["scheduled_pickup_at"],
                "updated_at": row["updated_at"],
                "cancel_reason": row["cancel_reason"],
                "events": events,
                "subscriptions": subscriptions,
            }
        return {"shipments": shipments}
    finally:
        conn.close()


def _ecommerce_snapshot() -> dict[str, Any]:
    conn = _connect_server("ecommerce")
    try:
        orders: list[dict[str, Any]] = []
        for row in _table(conn, "orders"):
            order_id = str(row["order_id"])
            detail = {
                **row,
                "subtotal_minor": int(row["subtotal_minor"]),
                "discount_minor": int(row["discount_minor"]),
                "shipping_minor": int(row["shipping_minor"]),
                "total_minor": int(row["total_minor"]),
                "items": [],
                "status_history": [],
                "refunds": [],
            }
            detail["items"] = [
                {**item, "qty": int(item["qty"]), "unit_price_minor": int(item["unit_price_minor"]), "line_total_minor": int(item["line_total_minor"])}
                for item in _table(conn, "order_items") if item.get("order_id") == order_id
            ]
            detail["status_history"] = [
                {"status": item["status"], "set_at": item["set_at"]}
                for item in _table(conn, "order_status_history") if item.get("order_id") == order_id
            ]
            orders.append(detail)
        return {"orders": orders}
    finally:
        conn.close()


def _email_snapshot() -> dict[str, Any]:
    conn = _connect_server("email")
    try:
        folders = {int(row["id"]): row["name"] for row in _table(conn, "folders")}
        messages: list[dict[str, Any]] = []
        for row in _table(conn, "messages"):
            try:
                to_addr = json.loads(row.get("to_addr_json") or "[]")
                cc_addr = json.loads(row.get("cc_addr_json") or "[]")
                bcc_addr = json.loads(row.get("bcc_addr_json") or "[]")
            except (TypeError, ValueError):
                to_addr, cc_addr, bcc_addr = [], [], []
            def csv(value: Any) -> str:
                return ", ".join(value) if isinstance(value, list) else str(value or "")
            messages.append({
                "email_id": str(row["id"]), "id": int(row["id"]), "folder": folders.get(int(row["folder_id"]), ""),
                "subject": row["subject"] or "", "from_addr": row["from_addr"] or "", "to_addr": csv(to_addr),
                "cc_addr": csv(cc_addr), "bcc_addr": csv(bcc_addr), "date": row["date"], "message_id": row["message_id"],
                "is_read": bool(int(row["is_read"])), "is_important": bool(int(row["is_important"])),
                "body_text": row["body_text"], "body_html": row["body_html"], "in_reply_to": row["in_reply_to"],
                "references": row["references_header"],
            })
        return {
            "inbox": [m for m in messages if m["folder"].lower() == "inbox"],
            "sent": [m for m in messages if m["folder"].lower() == "sent"],
            "drafts": [m for m in messages if m["folder"].lower() == "drafts"],
        }
    finally:
        conn.close()


def _direct_snapshot(workspace_root: Path | str, stage_idx: int) -> dict[str, Any]:
    return {
        "stage": int(stage_idx),
        "scenario_clock": _world_clock(),
        "banking": _banking_snapshot(),
        "calendar": _calendar_snapshot(),
        "delivery_logistics": _delivery_snapshot(),
        "ecommerce": _ecommerce_snapshot(),
        "email": _email_snapshot(),
        "legal_search": {},
        "listing_platform": _listing_snapshot(),
        "notification_hub": _notification_snapshot(),
        "workspace": _workspace_snapshot(workspace_root),
    }


def _live_snapshot(env: Any, stage_idx: int) -> dict[str, Any]:
    accounts = _live_call(env, "banking", "list_accounts", user_id=USER_ID)
    account_rows = _rows(accounts, "accounts", "items", "results")
    transactions = []
    for row in account_rows:
        account_id = row.get("account_id")
        if account_id:
            if str(account_id) == "acct_zl_renovation":
                transactions.extend(_rows(_live_call(env, "banking", "list_transactions", account_id=account_id, limit=400), "transactions", "items", "results"))
    calendars = _live_call(env, "calendar", "list_calendars", user_id=USER_ID)
    calendar_rows = _rows(calendars, "calendars", "items", "results")
    events = _live_call(env, "calendar", "list_events", calendar_id=CALENDAR_ID, max_results=500)
    notifications = _live_call(env, "notification_hub", "list_notifications", user_id=USER_ID, limit=500)
    shipments = _live_call(env, "delivery_logistics", "list_shipments", user_id=USER_ID, limit=500)
    shipment_rows = _rows(shipments, "shipments", "items", "results")
    shipment_details = {}
    for row in shipment_rows:
        shipment_id = row.get("shipment_id")
        if shipment_id:
            shipment_details[str(shipment_id)] = _live_call(env, "delivery_logistics", "get_shipment", shipment_id=str(shipment_id))
    orders = _live_call(env, "ecommerce", "list_orders", user_id=USER_ID, limit=100)
    order_rows = _rows(orders, "orders", "items", "results")
    order_details = []
    for row in order_rows:
        if row.get("order_id"):
            order_details.append(_live_call(env, "ecommerce", "get_order", order_id=str(row["order_id"])))
    inbox = _live_call(env, "email", "get_emails", folder="INBOX", page=1, page_size=100)
    sent = _live_call(env, "email", "get_emails", folder="Sent", page=1, page_size=100)
    listings = {LISTING_ID: _live_call(env, "listing_platform", "get_listing_detail", listing_id=LISTING_ID)}
    listing_rows = _rows(_live_call(env, "listing_platform", "search_listings", category="rent", city="Shanghai", district="Minhang", keyword="Hongqiao Jiayuan", limit=200), "listings", "items", "results")
    for row in listing_rows:
        if row.get("listing_id"):
            listings[str(row["listing_id"])] = _live_call(env, "listing_platform", "get_listing_detail", listing_id=str(row["listing_id"]))
    viewings = _live_call(env, "listing_platform", "list_viewings", user_id=USER_ID)
    return {
        "stage": int(stage_idx), "scenario_clock": _world_clock(),
        "banking": {"accounts": {str(row.get("account_id")): row for row in account_rows if row.get("account_id")}, "transactions": transactions},
        "calendar": {"calendars": calendar_rows, "events": _rows(events, "events", "items", "results")},
        "delivery_logistics": {"shipments": shipment_details},
        "ecommerce": {"orders": order_details},
        "email": {"inbox": _rows(inbox, "emails", "items", "results"), "sent": _rows(sent, "emails", "items", "results")},
        "legal_search": {},
        "listing_platform": {"listings": listings, "viewings": _rows(viewings, "viewings", "items", "results")},
        "notification_hub": {"notifications": _rows(notifications, "notifications", "items", "results")},
        "workspace": _workspace_snapshot_live(env),
    }


def capture_stage_snapshot(source: Any, stage_idx: int) -> dict[str, Any]:
    """Capture from direct SQLite paths in offline replay or live capabilities."""
    if isinstance(source, (str, Path)):
        return _direct_snapshot(source, stage_idx)
    return _live_snapshot(source, stage_idx)
