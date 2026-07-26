from __future__ import annotations

import json
from typing import Any

from loguru import logger

from ._helpers import (
    PERSISTENT_FILES,
    contains_all_groups,
    contains_any,
    read_file,
    reference_text,
    workspace_nonempty_count,
    workspace_text,
)

USER_ID = "user_lin_qiao"
TRAVELERS = ("LIN QIAO", "XU WEN CHENG")
ORGANIZER = "ops@galapagos-data.example"
US_AIRPORTS = {
    "ATL", "ANC", "BOS", "BWI", "CLT", "DCA", "DEN", "DFW", "DTW",
    "EWR", "FLL", "GUM", "HNL", "IAD", "IAH", "JFK", "LAS", "LAX",
    "MCO", "MIA", "MSP", "ORD", "PDX", "PHL", "PHX", "SAN", "SEA",
    "SFO", "SLC",
}
INACTIVE = {"cancelled", "canceled", "deleted", "expired", "failed", "refunded", "void"}
TICKETED = {"ticketed", "confirmed", "paid"}


def _call(env, server: str, tool: str, **kwargs: Any) -> Any:
    cap = getattr(env, f"{server}_mock", None)
    if cap is None:
        return None
    try:
        value = cap.call_tool(tool, **kwargs)
    except BaseException as exc:  # noqa: BLE001
        cause = exc
        while isinstance(cause, BaseExceptionGroup) and cause.exceptions:
            cause = cause.exceptions[0]
        logger.info(f"backend call {server}.{tool} failed: {type(cause).__name__}: {cause}")
        return None
    if isinstance(value, str):
        try:
            return json.loads(value)
        except json.JSONDecodeError:
            return value
    return value


def _flatten(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    if isinstance(value, (int, float, bool)):
        return str(value)
    if isinstance(value, dict):
        return "\n".join(f"{key}:{_flatten(item)}" for key, item in value.items())
    if isinstance(value, (list, tuple, set)):
        return "\n".join(_flatten(item) for item in value)
    return str(value)


def _has_groups(value: Any, groups: list[list[str]]) -> bool:
    text = _flatten(value).casefold()
    return all(any(str(term).casefold() in text for term in group) for group in groups)


def _has_any(value: Any, terms: list[str]) -> bool:
    text = _flatten(value).casefold()
    return any(str(term).casefold() in text for term in terms)


def _rows(value: Any) -> list[dict[str, Any]]:
    if isinstance(value, list):
        return [row for row in value if isinstance(row, dict)]
    if isinstance(value, dict):
        for key in (
            "items", "results", "bookings", "reservations", "events", "emails",
            "drafts", "hotels", "routes", "alerts", "forecast",
        ):
            rows = value.get(key)
            if isinstance(rows, list):
                return [row for row in rows if isinstance(row, dict)]
        return [value]
    return []


def _status(row: dict[str, Any]) -> str:
    return str(row.get("status") or row.get("booking_status") or "").casefold()


def _active(row: dict[str, Any]) -> bool:
    status = _status(row)
    return not any(token in status for token in INACTIVE)


def flight_bookings(env) -> list[dict[str, Any]]:
    return _rows(_call(env, "flight_booking", "list_bookings", user_id=USER_ID))


def active_flight_bookings(env) -> list[dict[str, Any]]:
    return [row for row in flight_bookings(env) if _active(row)]


def hotel_reservations(env) -> list[dict[str, Any]]:
    return _rows(_call(env, "hotel_booking", "list_reservations", user_id=USER_ID))


def active_hotel_reservations(env) -> list[dict[str, Any]]:
    return [row for row in hotel_reservations(env) if _active(row)]


def calendar_events(env) -> list[dict[str, Any]]:
    return _rows(
        _call(
            env,
            "calendar",
            "list_events",
            time_min="2026-08-14T00:00:00+08:00",
            time_max="2026-08-26T00:00:00+08:00",
            max_results=500,
        )
    )


def email_records(env, folder: str) -> list[dict[str, Any]]:
    records = _rows(_call(env, "email", "get_emails", folder=folder, page=1, page_size=100))
    detailed: list[dict[str, Any]] = []
    for row in records:
        email_id = row.get("email_id") or row.get("id")
        detail = _call(env, "email", "read_email", email_id=str(email_id)) if email_id else None
        detailed.append(detail if isinstance(detail, dict) else row)
    return detailed


def email_drafts(env) -> list[dict[str, Any]]:
    return _rows(_call(env, "email", "get_drafts", page=1, page_size=100))


def _segments(booking: dict[str, Any]) -> list[dict[str, Any]]:
    for key in ("segments", "itinerary", "legs", "flights"):
        value = booking.get(key)
        if isinstance(value, list):
            return [row for row in value if isinstance(row, dict)]
    return []


def _airport(segment: dict[str, Any], origin: bool) -> str:
    keys = ("origin", "origin_airport", "from", "departure_airport") if origin else (
        "dest", "destination", "destination_airport", "to", "arrival_airport"
    )
    for key in keys:
        value = segment.get(key)
        if value:
            return str(value).upper()
    return ""


def booking_airports(booking: dict[str, Any]) -> list[str]:
    airports: list[str] = []
    for segment in _segments(booking):
        origin = _airport(segment, True)
        destination = _airport(segment, False)
        if origin and (not airports or airports[-1] != origin):
            airports.append(origin)
        if destination:
            airports.append(destination)
    return airports


def booking_is_contiguous(booking: dict[str, Any]) -> bool:
    segments = _segments(booking)
    return bool(segments) and all(
        _airport(left, False) == _airport(right, True)
        for left, right in zip(segments, segments[1:])
    )


def booking_has_required_travelers(booking: dict[str, Any]) -> bool:
    return _has_groups(booking.get("passengers") or booking.get("travelers"), [[name] for name in TRAVELERS])


def all_active_bookings_avoid_us(env) -> bool:
    bookings = active_flight_bookings(env)
    return bool(bookings) and all(
        not (set(booking_airports(booking)) & US_AIRPORTS) for booking in bookings
    )


def _single_ticket_route(env, start: str, end: str, minimum_segments: int) -> dict[str, Any] | None:
    for booking in active_flight_bookings(env):
        airports = booking_airports(booking)
        if len(_segments(booking)) < minimum_segments or not booking_is_contiguous(booking):
            continue
        if not airports or airports[0] != start or airports[-1] != end:
            continue
        if booking.get("single_ticket") is False:
            continue
        if set(airports) & US_AIRPORTS:
            continue
        return booking
    return None


def outbound_single_ticket_complete(env) -> bool:
    booking = _single_ticket_route(env, "PVG", "GPS", 3)
    return booking is not None and booking_has_required_travelers(booking)


def return_single_ticket_complete(env) -> bool:
    booking = _single_ticket_route(env, "GPS", "PVG", 2)
    return booking is not None and booking_has_required_travelers(booking)


def required_travelers_ticketed(env) -> bool:
    outbound = _single_ticket_route(env, "PVG", "GPS", 3)
    inbound = _single_ticket_route(env, "GPS", "PVG", 2)
    return bool(outbound and inbound and booking_has_required_travelers(outbound) and booking_has_required_travelers(inbound))


def safe_outbound_held_or_ticketed(env) -> bool:
    return outbound_single_ticket_complete(env) and all_active_bookings_avoid_us(env)


def safe_ticketed_route_complete(env) -> bool:
    if not (outbound_single_ticket_complete(env) and return_single_ticket_complete(env) and all_active_bookings_avoid_us(env)):
        return False
    selected = [
        booking
        for booking in active_flight_bookings(env)
        if booking_airports(booking)[:1] in (["PVG"], ["GPS"])
    ]
    return bool(selected) and all(any(token in _status(row) for token in TICKETED) for row in selected)


def lodging_complete(env) -> bool:
    rows = active_hotel_reservations(env)
    return any(_has_any(row, ["Guayaquil", "GYE"]) for row in rows) and any(
        _has_any(row, ["Puerto Ayora"]) for row in rows
    )


def _refundable(row: dict[str, Any]) -> bool:
    if _has_any(row, ["nonrefundable", "non-refundable", "不可退"]):
        return False
    if row.get("refundable") is True:
        return True
    return _has_any(row, ["free_cancel", "refundable", "flex", "可取消"])


def hotel_authorization_integrity(env) -> bool:
    rows = active_hotel_reservations(env)
    if not rows or not any(_has_any(row, ["Puerto Ayora"]) for row in rows):
        return False
    for row in rows:
        if _refundable(row):
            continue
        decision = read_file(env, "/workspace/decision_log.md")
        if not contains_all_groups(
            decision,
            [["nonrefundable", "non-refundable", "不可退"], ["authorized", "approved", "林乔确认"]],
        ):
            return False
    return True


def registration_calendar_ready(env) -> bool:
    matches = [
        row
        for row in calendar_events(env)
        if _has_groups(row, [["Puerto Ayora"], ["2026-08-17", "8/17"], ["18:00"]])
    ]
    return len(matches) == 1 and bool(matches[0].get("reminders"))


def travel_window_calendar_ready(env) -> bool:
    text = _flatten(calendar_events(env))
    return _has_groups(text, [["2026-08-14"], ["17:30"], ["2026-08-25"], ["noon", "中午", "12:00"]])


def transfer_calendar_ready(env) -> bool:
    return any(
        _has_groups(row, [["GPS", "Baltra"], ["Puerto Ayora"], ["ferry", "渡轮", "transfer"]])
        for row in calendar_events(env)
    )


def weather_calendar_updated(env) -> bool:
    return any(
        _has_groups(row, [["weather", "marine", "天气"], ["swell", "wave", "风浪", "海况"]])
        for row in calendar_events(env)
    )


def organizer_source_ingested(env) -> bool:
    source = email_records(env, "INBOX")
    return any(
        _has_groups(row, [[ORGANIZER], ["LIN QIAO"], ["XU WEN CHENG"], ["2026-08-17"], ["18:00"]])
        for row in source
    ) and contains_all_groups(
        workspace_text(env), [["LIN QIAO"], ["XU WEN CHENG"], ["passport", "证件"], ["2026-08-17"], ["18:00"]]
    )


def organizer_confirmation_sent(env) -> bool:
    sent = email_records(env, "Sent")
    return any(
        _has_groups(row, [[ORGANIZER], ["LIN QIAO"], ["XU WEN CHENG"], ["Puerto Ayora"], ["2026-08-17"], ["18:00"]])
        and _has_any(row, ["sent", "folder:Sent", "已发送"])
        for row in sent
    )


def map_transfer_route_available(env) -> bool:
    data = _call(env, "maps", "directions", origin="GPS", destination="Puerto Ayora", mode="transit")
    return _has_groups(data, [["GPS"], ["Puerto Ayora"], ["ferry", "渡轮"]])


def weather_risk_available(env) -> bool:
    data = _call(env, "weather", "get_forecast", location="Puerto Ayora")
    if data is None:
        data = _call(env, "weather", "get_weather_forecast", location="Puerto Ayora")
    return _has_groups(data, [["Puerto Ayora"], ["swell", "wave", "marine", "风浪", "海况"]])


def payment_state_consistent(env) -> bool:
    if not safe_ticketed_route_complete(env) or not lodging_complete(env):
        return False
    flights_paid = all(
        _has_any(row, ["payment_status:paid", "paid", "已支付"])
        for row in active_flight_bookings(env)
        if booking_airports(row)[:1] in (["PVG"], ["GPS"])
    )
    hotels_authorized = all(
        _has_any(row, ["payment_status:frozen", "frozen", "authorized", "paid", "预授权"])
        for row in active_hotel_reservations(env)
    )
    return flights_paid and hotels_authorized


def budget_split_recorded(env) -> bool:
    return contains_all_groups(
        read_file(env, "/workspace/budget.md"),
        [["LIN QIAO", "林乔"], ["reimbursable", "报销"], ["XU WEN CHENG", "许闻"], ["private", "私人"]],
    )


def receipts_matrix_recorded(env) -> bool:
    text = read_file(env, "/workspace/evidence_log.md") + "\n" + read_file(env, "/workspace/final_summary.md")
    return contains_all_groups(
        text,
        [["flight", "航班"], ["hotel", "酒店"], ["TCT"], ["park fee", "国家公园"], ["transfer", "接送"], ["paid", "已付款"], ["frozen", "预授权"], ["pending", "待确认", "待退款"]],
    )


def persistent_artifacts_complete(env) -> bool:
    return workspace_nonempty_count(env) >= 6 and contains_all_groups(
        workspace_text(env),
        [["Galapagos", "加拉帕戈斯"], ["risk", "风险"], ["budget", "预算"], ["evidence", "receipt", "凭证"]],
    )


def final_summary_backend_consistent(env) -> bool:
    summary = read_file(env, "/workspace/final_summary.md")
    return (
        contains_all_groups(summary, [["actual", "实际"], ["no US", "无美国", "no-us"], ["Puerto Ayora"], ["registration", "登记"], ["hotel", "酒店"], ["receipt", "凭证"]])
        and safe_ticketed_route_complete(env)
        and required_travelers_ticketed(env)
        and hotel_authorization_integrity(env)
        and registration_calendar_ready(env)
        and payment_state_consistent(env)
    )


def passport_names_match(env) -> bool:
    return contains_all_groups(reference_text(env), [["LIN QIAO"], ["XU WEN CHENG"]]) and required_travelers_ticketed(env)


def departure_status_rechecked(env) -> bool:
    outbound = _single_ticket_route(env, "PVG", "GPS", 3)
    if outbound is None:
        return False
    segments = _segments(outbound)
    flight_no = str(segments[0].get("flight_no") or segments[0].get("number") or "")
    date = str(segments[0].get("date") or segments[0].get("departure_date") or "2026-08-14")
    if not flight_no:
        return False
    status = _call(env, "flight_booking", "get_flight_status", flight_no=flight_no, date=date)
    return _has_groups(status, [[flight_no], ["status", "scheduled", "delayed"]])
