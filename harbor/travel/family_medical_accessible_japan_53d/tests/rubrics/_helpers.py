from __future__ import annotations
import json
import re
from typing import Any

from harbor_evidence import EvidenceError
from harbor_evidence import snapshot as evidence_snapshot
from harbor_evidence import trace as evidence_trace

STAGE_COUNT = 25
WORKSPACE_FILES = (
    "trip_plan.md",
    "budget_ledger.md",
    "risk_register.md",
    "decision_log.md",
    "booking_register.md",
    "final_archive.md",
)

def snapshot(env, stage: int) -> dict[str, Any]:
    return evidence_snapshot(env, stage)


def trace(env, stage: int) -> list[dict[str, Any]]:
    return evidence_trace(env, stage)


def _active_stage(env) -> int:
    stage = int(getattr(env, "current_stage", STAGE_COUNT - 1))
    if not 0 <= stage < STAGE_COUNT:
        raise EvidenceError(f"active rubric stage out of range: {stage}")
    return stage


def _stage_snapshot(env) -> dict[str, Any]:
    return snapshot(env, _active_stage(env))

def _workspace_file_text(env, basename: str) -> str:
    files = _stage_snapshot(env).get("workspace")
    if not isinstance(files, dict):
        raise EvidenceError(f"stage {_active_stage(env)} snapshot has no workspace object")
    matches = [value for path, value in files.items() if str(path).rsplit("/", 1)[-1] == basename]
    if not matches:
        return ""
    value = matches[0]
    if not isinstance(value, str):
        raise EvidenceError(f"frozen workspace file {basename!r} is not text")
    return value.lower()

def _workspace_file_exists(env, basename: str) -> bool:
    return bool(_workspace_file_text(env, basename).strip())

def text_has(text: str, groups: list[list[str]]) -> bool:
    low = (text or "").lower()
    return all(any(w.lower() in low for w in g) for g in groups)

def _tool_calls(env, stage: int | None = None) -> list[dict[str, Any]]:
    stages = [stage] if stage is not None else range(STAGE_COUNT)
    out: list[dict[str, Any]] = []
    for stage_idx in stages:
        parsed = trace(env, stage_idx)
        out.extend(x for x in parsed if isinstance(x, dict))
    return out

def _norm_tool_name(name: str) -> str:
    return str(name or "").lower().replace("-", "_")

def _tool_name(call: dict[str, Any]) -> str:
    return _norm_tool_name(call.get("name") or "")

def _tool_args(call: dict[str, Any]) -> dict[str, Any]:
    args = call.get("arguments", {})
    return args if isinstance(args, dict) else {}

def _tool_calls_named(env, names: list[str], stage: int | None = None) -> list[dict[str, Any]]:
    wanted = {_norm_tool_name(n) for n in names}
    return [
        c
        for c in _tool_calls(env, stage)
        if c.get("success") is True and _tool_name(c) in wanted
    ]

def _tool_call_matches(env, names: list[str], predicate, stage: int | None = None) -> bool:
    return any(predicate(_tool_args(call)) for call in _tool_calls_named(env, names, stage))

def _tool_call_count(env, names: list[str], stage: int | None = None) -> int:
    return len(_tool_calls_named(env, names, stage))

def _jsonify(value: Any) -> Any:
    if value is None:
        return None
    if isinstance(value, (dict, list)):
        return value
    if isinstance(value, str):
        try:
            return json.loads(value)
        except Exception:
            return value
    return value

def _required(value: Any, where: str) -> Any:
    if value is None:
        raise EvidenceError(f"frozen snapshot did not capture {where}")
    if isinstance(value, dict) and set(value) == {"error"}:
        raise EvidenceError(f"frozen snapshot captured an error for {where}: {value['error']}")
    return value


def _trace_result(call: dict[str, Any]) -> Any:
    """Decode the MCP/ATIF result shapes retained in immutable trace evidence."""
    name = _tool_name(call) or "unknown tool"
    value = _jsonify(_required(call.get("result"), f"successful {name} trace result"))
    if isinstance(value, dict):
        structured = value.get("structuredContent", value.get("structured_content"))
        if isinstance(structured, dict) and "result" in structured:
            value = _jsonify(structured["result"])
        elif structured not in (None, {}):
            value = _jsonify(structured)
        elif isinstance(value.get("content"), list):
            blocks = value["content"]
            text = next(
                (
                    block.get("text")
                    for block in blocks
                    if isinstance(block, dict) and block.get("text") is not None
                ),
                None,
            )
            value = _jsonify(text) if text is not None else blocks
    if isinstance(value, dict) and value.get("error") not in (None, False, ""):
        raise EvidenceError(f"successful {name} trace contains an error: {value['error']}")
    return value


def _tool_call_results(env, names: list[str], predicate, stage: int | None = None) -> list[Any]:
    return [
        _trace_result(call)
        for call in _tool_calls_named(env, names, stage)
        if predicate(_tool_args(call))
    ]


def _rows(value: Any, *keys: str) -> list[dict[str, Any]]:
    if isinstance(value, list):
        return [row for row in value if isinstance(row, dict)]
    if isinstance(value, dict):
        for key in (*keys, "items"):
            rows = value.get(key)
            if isinstance(rows, list):
                return [row for row in rows if isinstance(row, dict)]
    return []


def money_fact(text: str, reference: str, amount: int | float, currency: str) -> bool:
    """Require one backend reference, currency and exact amount in a local clause."""
    normalized = (text or "").lower()
    reference = str(reference or "").lower()
    currency = str(currency or "").lower()
    if not reference or not currency:
        return False
    amount_value = float(amount)
    if not amount_value.is_integer():
        amount_pattern = re.escape(f"{amount_value:g}")
    else:
        digits = str(int(amount_value))
        amount_pattern = rf"{digits[:-3]},?{digits[-3:]}" if len(digits) > 3 else digits
    for clause in re.split(r"[\n;]", normalized):
        if reference in clause and currency in clause and re.search(rf"(?<!\d){amount_pattern}(?!\d)", clause):
            return True
    return False


def _search_rows(rows: list[dict[str, Any]], query: str) -> list[dict[str, Any]]:
    needle = query.strip().lower()
    if not needle:
        return rows
    return [row for row in rows if needle in json.dumps(row, ensure_ascii=False).lower()]


def _email_search_rows(
    rows: list[dict[str, Any]], details: Any, query: str
) -> list[dict[str, Any]]:
    """Replay the live email search (subject, from_addr, or body_text).

    The frozen get_emails listing is metadata-only, so a ref that only occurs in
    a message body cannot match the listing row. When the row itself does not
    match, fall back to the frozen read_email details captured for that
    message, which carry body_text.
    """
    needle = query.strip().lower()
    if not needle:
        return rows
    detail_map = details if isinstance(details, dict) else {}

    def matches(row: dict[str, Any]) -> bool:
        if needle in json.dumps(row, ensure_ascii=False).lower():
            return True
        email_id = row.get("email_id") or row.get("id")
        detail = detail_map.get(str(email_id)) if email_id is not None else None
        return isinstance(detail, dict) and needle in json.dumps(detail, ensure_ascii=False).lower()

    return [row for row in rows if matches(row)]


def _call(env, server: str, tool: str, **kwargs):
    section = _required(_stage_snapshot(env).get(server), f"{server} section")
    if not isinstance(section, dict):
        raise EvidenceError(f"frozen {server} section is not an object")

    if server == "flight_booking":
        if tool == "list_bookings":
            data = _required(section.get("bookings"), "flight_booking.list_bookings")
            rows = _rows(data, "bookings")
            status = kwargs.get("status")
            if status:
                rows = [row for row in rows if row.get("status") == status]
            return {"bookings": rows}
        if tool == "get_booking":
            return _required((section.get("booking_details") or {}).get(str(kwargs.get("pnr"))), "flight_booking.get_booking")
        if tool == "get_flight_offer":
            return _required((section.get("offers") or {}).get(str(kwargs.get("offer_id"))), "flight_booking.get_flight_offer")
        if tool in {"search_flights", "price_offer"}:
            return _required(section.get("search_results", section.get("offers")), f"flight_booking.{tool}")

    if server == "hotel_booking":
        if tool == "list_reservations":
            return _required(section.get("reservation_ids", section.get("reservations")), "hotel_booking.list_reservations")
        if tool == "get_reservation":
            return _required((section.get("reservations") or {}).get(str(kwargs.get("reservation_id"))), "hotel_booking.get_reservation")
        if tool == "get_hotel_details":
            return _required((section.get("hotels") or section.get("hotel_details") or {}).get(str(kwargs.get("hotel_id"))), "hotel_booking.get_hotel_details")
        if tool == "get_room_availability":
            hotel_id = str(kwargs.get("hotel_id"))
            book = section.get("availability")
            if isinstance(book, dict) and hotel_id in book:
                return book[hotel_id]
            if hotel_id == "jp_ht_001":
                return _required(section.get("kyoto_availability"), "hotel_booking.get_room_availability")
            return _required(None, "hotel_booking.get_room_availability")
        if tool == "search_hotels":
            return _required(section.get("search_results", section.get("hotels")), "hotel_booking.search_hotels")

    if server == "email":
        if tool in {"search_emails", "get_emails"}:
            folder = str(kwargs.get("folder") or "INBOX").lower()
            bucket = section.get(folder)
            listing = bucket.get("listing") if isinstance(bucket, dict) else bucket
            details = bucket.get("details") if isinstance(bucket, dict) else None
            rows = _email_search_rows(
                _rows(_required(listing, f"email.{folder}"), "emails", "results"),
                details,
                str(kwargs.get("query") or ""),
            )
            return {"emails": rows, "results": rows}
        if tool == "read_email":
            email_id = str(kwargs.get("email_id"))
            for bucket in section.values():
                if isinstance(bucket, dict) and isinstance(bucket.get("details"), dict) and email_id in bucket["details"]:
                    return bucket["details"][email_id]
            rows = _rows((section.get("inbox") or {}).get("listing"), "emails", "results")
            row = next((item for item in rows if str(item.get("email_id") or item.get("id")) == email_id), None)
            return _required(row, "email.read_email")
        if tool == "get_drafts":
            return _required(section.get("drafts"), "email.get_drafts")

    if server == "calendar" and tool == "search_events":
        data = section.get("events", section.get("wedding_events"))
        rows = _search_rows(_rows(_required(data, "calendar.search_events"), "events", "results"), str(kwargs.get("query") or ""))
        return rows

    if server == "credit_card":
        if tool == "list_cards":
            return _required(section.get("cards"), "credit_card.list_cards")
        if tool == "get_card":
            card_id = str(kwargs.get("card_id"))
            details = section.get("card_details") or {}
            if isinstance(details, dict) and card_id in details:
                return details[card_id]
            primary = section.get("primary_card")
            if isinstance(primary, dict) and primary.get("card_id") == card_id:
                return primary
            match = next((row for row in _rows(section.get("cards"), "cards") if row.get("card_id") == card_id), None)
            return _required(match, "credit_card.get_card")

    if server == "notion":
        if tool == "API-post-search":
            query = str(kwargs.get("query") or "")
            indexed = section.get("query_results") or {}
            if isinstance(indexed, dict) and query in indexed:
                return indexed[query]
            data = _required(section.get("search"), "notion.API-post-search")
            rows = _search_rows(_rows(data, "results"), query)
            return {"results": rows}
        if tool == "API-get-block-children":
            return _required((section.get("blocks") or {}).get(str(kwargs.get("block_id"))), "notion.API-get-block-children")

    if server == "rail_booking":
        if tool == "get_train_status":
            return _required(section.get("maintenance"), "rail_booking.get_train_status")
        if tool == "search_trains":
            origin = str(kwargs.get("origin") or "").lower()
            key = "kansai_routes" if origin == "kyoto" else "safe_offer"
            return _required(section.get(key), "rail_booking.search_trains")
        if tool == "list_train_bookings":
            return _required(section.get("bookings"), "rail_booking.list_train_bookings")

    if server == "visa_and_advisory":
        if tool in {"check_entry_requirements", "get_advisory"}:
            return _required(section.get("entry"), f"visa_and_advisory.{tool}")
        if tool == "list_visa_applications":
            return _required(section.get("passports"), "visa_and_advisory.list_visa_applications")

    if server == "weather":
        if tool == "get_alerts":
            alerts = section.get("alerts")
            if isinstance(alerts, dict) and str(kwargs.get("geo") or "").lower() in alerts:
                return alerts[str(kwargs.get("geo")).lower()]
            return _required(alerts, "weather.get_alerts")
        if tool == "get_forecast_daily":
            forecasts = section.get("forecasts")
            geo = str(kwargs.get("geo") or "").lower()
            if isinstance(forecasts, dict) and geo in forecasts:
                return forecasts[geo]
            if geo == "kyoto":
                return _required(section.get("forecast"), "weather.get_forecast_daily")
            return _required(None, "weather.get_forecast_daily")

    if server == "maps":
        if tool == "search_places":
            data = section.get("search_results", section.get("accessible_routes"))
            return _required(data, "maps.search_places")
        if tool == "get_place_details":
            return _required((section.get("places") or section.get("place_details") or {}).get(str(kwargs.get("place_id"))), "maps.get_place_details")

    raise EvidenceError(f"frozen snapshot has no projection for {server}.{tool}")


def _call_json(env, server: str, tool: str, **kwargs):
    return _jsonify(_call(env, server, tool, **kwargs))

def _flight_bookings(env, **kwargs) -> list[dict[str, Any]]:
    # Target bookings are created with contact.email as user_id/email.  Never
    # score against the hundreds of unrelated fixture bookings in the catalog.
    if "user_id" not in kwargs and "email" not in kwargs:
        kwargs["email"] = "liwei@example.com"
    data = _call_json(env, "flight_booking", "list_bookings", page=1, page_size=50, **kwargs)
    if isinstance(data, dict):
        rows = data.get("bookings", [])
        return rows if isinstance(rows, list) else []
    return []

def _flight_booking_details(env, **kwargs) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for row in _flight_bookings(env, **kwargs):
        pnr = row.get("pnr")
        if not pnr:
            raise ValueError("flight booking summary missing pnr")
        detail = _call_json(env, "flight_booking", "get_booking", pnr=pnr)
        if not isinstance(detail, dict) or detail.get("pnr") != pnr:
            raise ValueError(f"invalid flight booking detail for {pnr}")
        out.append(detail)
    return out

def _hotel_reservations(env, user_id: str = "trav_liwei") -> list[dict[str, Any]]:
    data = _call_json(env, "hotel_booking", "list_reservations", user_id=user_id)
    if isinstance(data, dict):
        rows = data.get("reservations", data.get("results"))
        if isinstance(rows, list):
            return rows
        ids = data.get("reservation_ids", [])
        if isinstance(ids, list):
            return [{"reservation_id": rid} for rid in ids if rid]
        return []
    if isinstance(data, list):
        return data
    return []

def _hotel_reservation_details(env, user_id: str = "trav_liwei") -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for row in _hotel_reservations(env, user_id=user_id):
        rid = row.get("reservation_id")
        if not rid:
            continue
        detail = _call_json(env, "hotel_booking", "get_reservation", reservation_id=rid)
        if isinstance(detail, dict):
            out.append(detail)
    return out

def _cards(env, user_id: str = "trav_liwei") -> list[dict[str, Any]]:
    data = _call_json(env, "credit_card", "list_cards", user_id=user_id)
    return data if isinstance(data, list) else []

def _card_detail(env, card_id: str) -> dict[str, Any]:
    data = _call_json(env, "credit_card", "get_card", card_id=card_id)
    return data if isinstance(data, dict) else {}
