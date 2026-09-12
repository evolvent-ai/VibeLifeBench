"""Freeze the live San Francisco summit world through its eight MCP services."""
from __future__ import annotations

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Any

USER_ID = "liming@company.com"
TRIP_ACCOUNT = "ACC_TRIP"
NOTION_PAGE_ID = "PAGE_TRIP"
CLOCK = Path(os.environ.get("WORLD_CLOCK_FILE", "/world-clock/current.json"))
BASELINE = {"AGENTS.md", "ARTIFACT_CONTRACT.md", "PERSONA.md", "TOOLS.md", "USER.md"}


def _decode(value: Any) -> Any:
    if isinstance(value, str):
        try:
            return json.loads(value)
        except json.JSONDecodeError:
            return value
    return value


def _unwrap_envelope(value: Any, fetch_page=None) -> Any:
    if not isinstance(value, dict):
        return value
    rows = value.get("items")
    if not isinstance(rows, list):
        return value
    if "total" not in value and "has_more" not in value:
        return value
    merged = list(rows)
    total_value = value.get("total")
    total = int(total_value) if isinstance(total_value, (int, float)) else None
    current, page = value, int(value.get("page") or 1)
    while fetch_page is not None and current.get("has_more"):
        page += 1
        nxt = fetch_page(page)
        if not isinstance(nxt, dict) or not isinstance(nxt.get("items"), list):
            break
        fresh = nxt["items"]
        if not fresh:
            break
        merged.extend(fresh)
        current = nxt
        if total is not None and len(merged) >= total:
            break
    if (total is not None and len(merged) < total) or current.get("has_more"):
        return {"items": merged, "_pagination_incomplete": True,
                "_captured": len(merged), "_total": total}
    return merged


def _call(env: Any, server: str, tool: str, **kwargs: Any) -> Any:
    cap = getattr(env, f"{server}_mock", None)
    if cap is None:
        return {"error": f"missing capability: {server}"}
    try:
        first = _decode(cap.call_tool(tool, **kwargs))
        return _unwrap_envelope(
            first, lambda page: _decode(cap.call_tool(tool, **{**kwargs, "page": page})),
        )
    except BaseException as exc:  # noqa: BLE001
        return {"error": f"{type(exc).__name__}: {exc}"}


def _paged_call(env: Any, server: str, tool: str, *, rows_key: str,
                id_keys: tuple[str, ...], **kwargs: Any) -> Any:
    """Collect service-specific envelopes, notably email's clamped pages."""
    first = _call(env, server, tool, page=1, page_size=50, **kwargs)
    if not isinstance(first, dict) or first.get("error"):
        return first
    rows = list(first.get(rows_key) or [])
    total_value = first.get("total_results", first.get("total", len(rows)))
    total = int(total_value) if isinstance(total_value, (int, float)) else len(rows)

    def row_id(row: Any) -> str:
        if not isinstance(row, dict):
            return ""
        return next((str(row[key]) for key in id_keys if row.get(key) is not None), "")

    seen, page = {row_id(row) for row in rows}, 2
    while len(rows) < total:
        nxt = _call(env, server, tool, page=page, page_size=50, **kwargs)
        if not isinstance(nxt, dict) or nxt.get("error"):
            break
        fresh = [row for row in (nxt.get(rows_key) or []) if row_id(row) not in seen]
        if not fresh:
            break
        rows.extend(fresh)
        seen.update(row_id(row) for row in fresh)
        page += 1
    first[rows_key] = rows
    first["captured_count"] = len(rows)
    first["captured_complete"] = len(rows) >= total
    return first


def _workspace(env: Any) -> dict[str, str]:
    fs = getattr(getattr(env, "workspace", None), "fs", None)
    if fs is None:
        return {}
    output: dict[str, str] = {}
    seen: set[str] = set()

    def walk(path: str, depth: int) -> None:
        if path in seen or len(output) >= 200:
            return
        seen.add(path)
        name = path.rsplit("/", 1)[-1]
        if name.startswith(".") or name in BASELINE:
            return
        if name.lower().endswith((".md", ".txt", ".json", ".csv")):
            try:
                raw = fs.read_file(path)
            except Exception:  # noqa: BLE001
                return
            text = raw.decode("utf-8", errors="replace") if isinstance(raw, bytes) else str(raw)
            if text.strip():
                output[path] = text[:200000]
            return
        if depth:
            try:
                for child in fs.list_dir(path):
                    walk(f"{path.rstrip('/')}/{child}", depth - 1)
            except Exception:  # noqa: BLE001
                pass

    walk("/workspace", 4)
    return output


def _world_clock() -> dict[str, str]:
    payload = json.loads(CLOCK.read_text(encoding="utf-8"))
    if not isinstance(payload, dict) or set(payload) != {"world_now"}:
        raise RuntimeError("world clock must contain exactly world_now")
    value = payload["world_now"]
    if not isinstance(value, str):
        raise RuntimeError("world_now must be a string")
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        raise RuntimeError("world_now must include a timezone")
    return {"world_now": value}


def _email_folder(env: Any, folder: str, *, details: bool) -> dict[str, Any]:
    listing = _paged_call(env, "email", "get_emails", rows_key="emails",
                          id_keys=("email_id", "id"), folder=folder)
    captured: dict[str, Any] = {}
    if details and isinstance(listing, dict):
        for row in listing.get("emails") or []:
            email_id = row.get("email_id") or row.get("id") if isinstance(row, dict) else None
            if email_id is None:
                continue
            detail = _call(env, "email", "read_email", email_id=str(email_id))
            headers = _call(env, "email", "get_email_headers", email_id=str(email_id))
            if isinstance(detail, dict) and isinstance(headers, dict):
                for key in ("in_reply_to", "references", "references_header", "headers", "thread_id"):
                    if headers.get(key) is not None:
                        detail.setdefault(key, headers[key])
            captured[str(email_id)] = detail
    return {"listing": listing, "details": captured}


def _booking_snapshot(env: Any) -> dict[str, Any]:
    listing = _call(env, "flight_booking", "list_bookings", email=USER_ID)
    rows = listing if isinstance(listing, list) else (
        listing.get("bookings", listing.get("pnrs", [])) if isinstance(listing, dict) else [])
    details = {}
    for row in rows or []:
        pnr = row.get("pnr") if isinstance(row, dict) else None
        if pnr:
            details[str(pnr)] = _call(env, "flight_booking", "get_booking", pnr=str(pnr))
    return {"bookings": listing, "booking_details": details}


def _hotel_snapshot(env: Any) -> dict[str, Any]:
    listing = _call(env, "hotel_booking", "list_reservations", user_id=USER_ID)
    rows = listing if isinstance(listing, list) else (
        listing.get("reservation_ids", listing.get("reservations", []))
        if isinstance(listing, dict) else [])
    details = {}
    for row in rows or []:
        reservation_id = row.get("reservation_id") if isinstance(row, dict) else row
        if reservation_id:
            details[str(reservation_id)] = _call(
                env, "hotel_booking", "get_reservation", reservation_id=str(reservation_id))
    return {"reservations": listing, "reservation_details": details}


def _visa_snapshot(env: Any) -> dict[str, Any]:
    applications = _call(env, "visa_and_advisory", "list_visa_applications", user_id=USER_ID)
    rows = applications if isinstance(applications, list) else (
        applications.get("applications", []) if isinstance(applications, dict) else [])
    details = {}
    for row in rows or []:
        application_id = row.get("application_id") if isinstance(row, dict) else None
        if application_id:
            details[str(application_id)] = _call(
                env, "visa_and_advisory", "get_visa_application",
                application_id=str(application_id))
    return {
        "applications": applications,
        "application_details": details,
        "entry_requirements": _call(
            env, "visa_and_advisory", "check_entry_requirements",
            nationality="CN", destination="US", purpose="business", transit_countries=["HK"]),
        "advisory": _call(env, "visa_and_advisory", "get_advisory", country_code="US"),
    }


def _notion_snapshot(env: Any) -> dict[str, Any]:
    search = _call(env, "notion", "API-post-search",
                   query="Ming Lin 2026 San Francisco Summit",
                   filter={"value": "page"}, page_size=100)
    pages = search.get("results", []) if isinstance(search, dict) else (
        search if isinstance(search, list) else [])
    if not pages:
        page = _call(env, "notion", "API-retrieve-a-page", page_id=NOTION_PAGE_ID)
        pages = [page] if isinstance(page, dict) and not page.get("error") else []
    return {
        "search": search,
        "pages": pages,
        "blocks": {
            str(page.get("id", NOTION_PAGE_ID)): _call(
                env, "notion", "API-get-block-children",
                block_id=str(page.get("id", NOTION_PAGE_ID)), page_size=100)
            for page in pages[:10] if isinstance(page, dict)
        },
    }


def capture_stage_snapshot(env: Any, stage_idx: int) -> dict[str, Any]:
    return {
        "stage": int(stage_idx), "world_clock": _world_clock(), "workspace": _workspace(env),
        "flight_booking": _booking_snapshot(env),
        "hotel_booking": _hotel_snapshot(env),
        "visa_and_advisory": _visa_snapshot(env),
        "calendar": {"events": _call(
            env, "calendar", "list_events", time_min="2025-01-01T00:00:00+08:00",
            time_max="2026-12-31T23:59:59+08:00", max_results=250)},
        "email": {
            "inbox": _email_folder(env, "INBOX", details=False),
            "sent": _email_folder(env, "Sent", details=True),
            "drafts": _paged_call(env, "email", "get_drafts",
                                    rows_key="drafts", id_keys=("draft_id", "id")),
        },
        "banking": {
            "account": _call(env, "banking", "get_account", account_id=TRIP_ACCOUNT),
            "transactions": _call(env, "banking", "list_transactions",
                                  account_id=TRIP_ACCOUNT, limit=500),
        },
        "notion": _notion_snapshot(env),
        "health_tracker": {
            "goals": _call(env, "health_tracker", "get_goals", user_id=USER_ID, status="active"),
            "metrics": _call(env, "health_tracker", "get_metrics", user_id=USER_ID,
                             type="weight", since="2026-01-01", until="2026-04-30"),
        },
    }
