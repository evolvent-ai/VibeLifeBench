"""Shared helpers backed exclusively by Harbor's frozen stage evidence."""
from __future__ import annotations

import json
from typing import Any

from harbor_evidence import response as evidence_response
from harbor_evidence import snapshot as evidence_snapshot

from loguru import logger


# ── core ────────────────────────────────────────────────────────────


class RubricInfrastructureError(RuntimeError):
    """A required grader read path is unavailable or returned invalid data."""


def _stage(env) -> int:
    stage = getattr(env, "current_stage", None)
    if stage is not None:
        return int(stage)
    stages = env.published_stages()
    if not stages:
        raise RubricInfrastructureError("no published stage evidence")
    return max(stages)


def _snapshot(env) -> dict[str, Any]:
    return evidence_snapshot(env, _stage(env))


def _listing(value: Any, *keys: str) -> Any:
    if isinstance(value, dict):
        for key in keys:
            if key in value:
                return value[key]
    return value


def _call(env, server: str, tool: str, **kwargs: Any) -> Any:
    """Resolve the historical result of a service call from the stage snapshot."""
    world = _snapshot(env)
    service = world.get(server)
    if not isinstance(service, dict):
        # A valid but empty fixture may omit untouched services.  Treat that as
        # an empty world; malformed stage files are rejected by HarborEvidence.
        service = {}

    if server == "flight_booking":
        if tool == "list_bookings":
            return service.get("listing")
        if tool == "get_booking":
            details = service.get("details") or {}
            return details.get(str(kwargs.get("pnr")))
        if tool == "search_flights":
            # Search results are transient and are not part of the frozen world;
            # the captured booking state remains the authoritative evidence.
            return []
    elif server == "hotel_booking":
        if tool == "list_reservations":
            return service.get("listing")
        if tool == "get_reservation":
            details = service.get("details") or {}
            return details.get(str(kwargs.get("reservation_id")))
    elif server == "visa_and_advisory":
        if tool == "list_visa_applications":
            apps_by_user = service.get("applications_by_user")
            user_id = str(kwargs.get("user_id") or "li_wei")
            if isinstance(apps_by_user, dict) and user_id in apps_by_user:
                frozen = apps_by_user.get(user_id)
                return frozen if isinstance(frozen, list) else []
            return service.get("applications")
        if tool == "list_visa_products":
            return []
    elif server == "calendar":
        if tool == "list_calendars":
            calendars = service.get("calendars")
            return service.get("listing") if calendars is None else calendars
        if tool == "list_events":
            return service.get("events")
    elif server == "notion":
        if tool == "API-post-search":
            return service.get("search")
        if tool == "API-get-block-children":
            blocks = service.get("blocks") or {}
            block_id = str(kwargs.get("block_id"))
            return blocks.get(block_id) or next(iter(blocks.values()), None)
    elif server == "email":
        if tool == "get_emails":
            folder = str(kwargs.get("folder") or "INBOX").lower()
            if folder in {"sent", "inbox.sent", "sent items"}:
                box = service.get("sent")
            else:
                box = service.get("inbox")
            return box.get("listing") if isinstance(box, dict) else box
        if tool == "get_drafts":
            return service.get("drafts")
        if tool == "search_emails":
            query = str(kwargs.get("query") or "").lower()
            folder = str(kwargs.get("folder") or "").lower()
            box = service.get("sent") if folder in {"sent", "inbox.sent", "sent items"} else service.get("inbox")
            listing = box.get("listing") if isinstance(box, dict) else box
            rows = _listing(listing, "emails", "messages")
            details = box.get("details") if isinstance(box, dict) else {}
            hits = []
            for row in rows or []:
                item = details.get(str(row.get("email_id") or row.get("id")), row) if isinstance(row, dict) else row
                if query in json.dumps(item, ensure_ascii=False, default=str).lower():
                    hits.append(item)
            return {"emails": hits, "total_results": len(hits)}

    raise RubricInfrastructureError(f"unsupported frozen read: {server}.{tool}")


def _any_kw(text: str, needles: list[str]) -> bool:
    if not text:
        return False
    low = text.lower()
    return any(n.lower() in low for n in needles)


# ── flight / hotel / visa ──────────────────────────────────────────


def _list_flight_bookings(env) -> list[dict]:
    data = _call(env, "flight_booking", "list_bookings", user_id="li_wei")
    if isinstance(data, dict):
        return list(data.get("bookings") or data.get("items") or [])
    if isinstance(data, list):
        return list(data)
    return []


# Backwards-compatible alias used by stage_0.
list_flight_bookings = _list_flight_bookings


def _list_hotel_reservations(env) -> list[dict]:
    """Return the detailed hotel records frozen with the stage."""
    data = _call(env, "hotel_booking", "list_reservations", user_id="li_wei")
    service = _snapshot(env).get("hotel_booking") or {}
    details_map = service.get("details") if isinstance(service, dict) else {}
    if isinstance(details_map, dict) and details_map:
        return [d for d in details_map.values() if isinstance(d, dict)]
    details: list[dict] = []
    if isinstance(data, dict):
        rids = data.get("reservation_ids") or data.get("reservations") or []
        for rid in rids[:15]:
            rid = rid.get("reservation_id") if isinstance(rid, dict) else rid
            d = _call(env, "hotel_booking", "get_reservation", reservation_id=rid)
            if isinstance(d, dict):
                details.append(d)
    elif isinstance(data, list):
        for r in data[:15]:
            if isinstance(r, dict):
                if "reservation_id" in r and ("price" in r or "total_charged" in r):
                    details.append(r)
                else:
                    rid = r.get("reservation_id") or r.get("id")
                    if rid:
                        d = _call(env, "hotel_booking", "get_reservation",
                                  reservation_id=rid)
                        if isinstance(d, dict):
                            details.append(d)
    return details


def _list_visa_apps(env, user_id: str = "li_wei") -> list[dict]:
    data = _call(env, "visa_and_advisory", "list_visa_applications", user_id=user_id)
    if isinstance(data, list):
        return data
    if isinstance(data, dict):
        return list(data.get("applications") or [])
    return []


# ── calendar ───────────────────────────────────────────────────────


def _calendar_list(env) -> list[dict] | None:
    data = _call(env, "calendar", "list_calendars", user_id="li_wei")
    if data is None:
        return []
    if isinstance(data, dict) and data.get("error"):
        raise RubricInfrastructureError(
            f"calendar list capture failed: {data['error']}"
        )
    cals: list = []
    if isinstance(data, list):
        cals = data
    elif isinstance(data, dict):
        cals = (
            data.get("calendars")
            or data.get("results")
            or data.get("items")
            or []
        )
    out: list[dict] = []
    for c in cals:
        if not isinstance(c, dict):
            continue
        out.append({
            "id": c.get("calendar_id") or c.get("id") or "",
            "calendar_id": c.get("calendar_id") or c.get("id") or "",
            "name": c.get("name") or c.get("displayname") or "",
            "displayname": c.get("name") or c.get("displayname") or "",
            "timezone": c.get("timezone") or "",
            "is_primary": bool(c.get("is_primary", False)),
        })
    return out


# Backwards-compatible alias used by stage_0.
calendar_list = _calendar_list


def _all_calendar_events(env) -> list[dict] | None:
    """Return captured events without inventing an unavailable calendar list."""
    data = _call(
        env, "calendar", "list_events", calendar_id="cal_000001", max_results=500
    )
    if data is None:
        return None
    if isinstance(data, dict) and data.get("error"):
        raise RubricInfrastructureError(
            f"calendar event capture failed: {data['error']}"
        )
    if isinstance(data, list):
        return list(data)
    if isinstance(data, dict):
        return list(
            data.get("events") or data.get("results") or data.get("items") or []
        )
    raise RubricInfrastructureError(
        f"calendar event capture has invalid type: {type(data).__name__}"
    )


def _calendar_events(env, calendar_name: str) -> list[dict] | None:
    cals = _calendar_list(env)
    if cals is None:
        return None
    calendar_ids = {
        str(c.get("calendar_id") or c.get("id") or "")
        for c in cals
        if (c.get("name") or c.get("displayname") or "").lower()
        == calendar_name.lower()
    }
    if not calendar_ids:
        return []
    events = _all_calendar_events(env)
    if events is None:
        return None
    return [
        event
        for event in events
        if not event.get("calendar_id")
        or str(event.get("calendar_id")) in calendar_ids
    ]


# Backwards-compatible alias used by stage_0.
calendar_events = _calendar_events


# ── notion ─────────────────────────────────────────────────────────


def _notion_body(env) -> str | None:
    """Full text of the Li Wei trip journal Notion page. None if unreachable."""
    search = _call(env, "notion", "API-post-search", query="Japan Trip 2026")
    page_id = None
    if isinstance(search, dict):
        for r in search.get("results") or []:
            if isinstance(r, dict) and r.get("object") == "page":
                page_id = r.get("id")
                break
    if not page_id:
        return None
    blocks = _call(env, "notion", "API-get-block-children", block_id=page_id)
    if blocks is None:
        return None
    chunks: list[str] = []
    items = blocks.get("results") if isinstance(blocks, dict) else blocks
    for block in items or []:
        if not isinstance(block, dict):
            continue
        block_type = block.get("type") or ""
        type_data = block.get(block_type) or {}
        if not isinstance(type_data, dict):
            continue
        for rt in type_data.get("rich_text") or []:
            if not isinstance(rt, dict):
                continue
            text = rt.get("plain_text")
            if not text and isinstance(rt.get("text"), dict):
                text = rt["text"].get("content")
            if text:
                chunks.append(str(text))
    return "\n".join(chunks)


def _notion_text(env) -> str:
    body = _notion_body(env)
    return (body or "").strip()


def _notion_agent_text(env) -> str:
    """Read only trip-journal blocks created or edited after the kickoff.

    Blocks are aggregated across every frozen page so evidence is not lost
    when an agent creates or renames its own journal page; the kickoff-date
    filter keeps seeded (pre-kickoff) content out of the agent corpus.
    """
    world = _snapshot(env).get("notion") or {}
    blocks_by_page = world.get("blocks") if isinstance(world, dict) else None
    chunks: list[str] = []
    pages: list = []
    if isinstance(blocks_by_page, dict) and blocks_by_page:
        pages = list(blocks_by_page.values())
    else:
        # Older snapshots: fall back to the frozen search's first page.
        search = _call(env, "notion", "API-post-search", query="Japan Trip 2026")
        page_id = None
        if isinstance(search, dict):
            for result in search.get("results") or []:
                if isinstance(result, dict) and result.get("object") == "page":
                    page_id = result.get("id")
                    break
        if page_id:
            fetched = _call(env, "notion", "API-get-block-children", block_id=page_id)
            if fetched is not None:
                pages.append(fetched)
    for blocks in pages:
        items = blocks.get("results") if isinstance(blocks, dict) else blocks
        for block in items or []:
            if not isinstance(block, dict):
                continue
            created = str(block.get("created_time") or "")
            edited = str(block.get("last_edited_time") or "")
            if max(created, edited) < "2026-04-17":
                continue
            block_type = block.get("type") or ""
            type_data = block.get(block_type) or {}
            if not isinstance(type_data, dict):
                continue
            for rich_text in type_data.get("rich_text") or []:
                if not isinstance(rich_text, dict):
                    continue
                text = rich_text.get("plain_text")
                if not text and isinstance(rich_text.get("text"), dict):
                    text = rich_text["text"].get("content")
                if text:
                    chunks.append(str(text))
    return "\n".join(chunks)


# ── workspace ──────────────────────────────────────────────────────


_WORKSPACE_SCAN_PATHS = (
    "/workspace/HEARTBEAT.md",
    "/workspace/itinerary.md",
    "/workspace/expense_summary.md",
    "/workspace/packing_briefing.md",
    "/workspace/weather_alerts.log",
)


def _workspace_text(env) -> str:
    workspace = _snapshot(env).get("workspace")
    if not isinstance(workspace, dict):
        return ""
    chunks: list[str] = []
    for p in _WORKSPACE_SCAN_PATHS:
        value = workspace.get(p)
        if isinstance(value, str) and value:
            chunks.append(value)
    return "\n".join(chunks)


def _workspace_file_text(env, path: str) -> str:
    workspace = _snapshot(env).get("workspace")
    if not isinstance(workspace, dict):
        return ""
    value = workspace.get(path, "")
    return value if isinstance(value, str) else str(value or "")


def _all_corpus(env) -> str:
    """Lowercase corpus of Agent-authored Notion blocks plus workspace notes."""
    return (_notion_agent_text(env) + "\n" + _workspace_text(env)).lower()


# Backwards-compatible aliases used by stage_0 / final.
all_corpus = _all_corpus
notion_body = _notion_body
notion_text = _notion_text
workspace_text = _workspace_text


# ── email ──────────────────────────────────────────────────────────


def _merge_frozen_details(box: Any, rows: list) -> list:
    """Fold the frozen read_email details (body_text, headers) into the frozen
    listing rows. The list view never carries bodies, but the capture freezes
    them alongside, so checkers can match on real message content.
    """
    details = box.get("details") if isinstance(box, dict) else {}
    if not isinstance(details, dict) or not details:
        return rows
    out = []
    for row in rows:
        if isinstance(row, dict):
            detail = details.get(str(row.get("email_id") or row.get("id")))
            if isinstance(detail, dict):
                merged = dict(row)
                for key in ("body_text", "body_html", "from_addr"):
                    if detail.get(key) is not None:
                        merged.setdefault(key, detail.get(key))
                out.append(merged)
                continue
        out.append(row)
    return out


def _emails_for(env, user: str = "li_wei") -> list[dict] | None:
    """List inbox emails for ``user`` or None if backend unreachable."""
    data = _call(env, "email", "get_emails", folder="INBOX")
    if data is None:
        return None
    rows: list = []
    if isinstance(data, list):
        rows = list(data)
    elif isinstance(data, dict):
        rows = list(data.get("emails") or data.get("messages") or [])
    service = _snapshot(env).get("email") or {}
    box = service.get("inbox") if isinstance(service, dict) else None
    return _merge_frozen_details(box, rows)


# Backwards-compatible alias used by final.
emails_for = _emails_for


def _sent_email_rows(env, user: str = "li_wei") -> list[dict]:
    """Sent-folder rows enriched with frozen bodies; [] when absent."""
    data = _sent_emails(env, user)
    if not data:
        return []
    service = _snapshot(env).get("email") or {}
    box = service.get("sent") if isinstance(service, dict) else None
    return _merge_frozen_details(box, list(data))


def _sent_emails_any(env, user: str = "li_wei") -> list[dict]:
    """Compatibility wrapper for checks where an absent Sent box means no hit."""
    return _sent_emails(env, user) or []


def _sent_emails(env, user: str = "li_wei") -> list[dict] | None:
    """Return the single frozen Sent listing, preserving unreachable state."""
    data = _call(env, "email", "get_emails", folder="Sent")
    if data is None:
        return None
    if isinstance(data, dict) and data.get("error"):
        raise RubricInfrastructureError(f"Sent capture failed: {data['error']}")
    if isinstance(data, list):
        return list(data)
    if isinstance(data, dict):
        return list(data.get("emails") or data.get("messages") or [])
    raise RubricInfrastructureError(
        f"Sent capture has invalid type: {type(data).__name__}"
    )


# ── cron / turn-log (NOT IMPLEMENTED — graceful empty) ─────────────


def _cron_reminders(env) -> list[dict]:
    """Cron-store is not implemented — always returns []."""
    return []


def _turn_log(env) -> list[dict]:
    """Turn-log is not maintained — always returns []. The three checkers
    that *require* turn_log content (s8_weather_monitoring_cron,
    s10_typhoon_acknowledged, six_of_nine_services_used) are intentionally
    omitted from CHECKS lists.
    """
    return []


def _agent_responses(env, *, stage: int | None = None,
                     event_id: str | None = None) -> str:
    """Return assistant text captured for a frozen stage."""
    return evidence_response(env, _stage(env) if stage is None else int(stage))


# ── budget FX (was mock_env.fx in v3) ──────────────────────────────

# 1 CNY = 20 JPY (fixed rate, per v3 harness/fx.py).
_FX_RATES_TO_CNY: dict[str, float] = {
    "CNY": 1.0,
    "JPY": 1.0 / 20.0,
    "USD": 7.2,
}


def to_cny(amount: float, currency: str) -> float:
    """Convert ``amount`` in ``currency`` to CNY. Raises KeyError on unknown."""
    rate = _FX_RATES_TO_CNY[currency.upper()]
    return amount * rate
