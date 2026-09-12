"""Final rubric: backend objects and durable artifacts must agree field-by-field."""
from __future__ import annotations

from loguru import logger

from .shared._helpers import list_flight_bookings, list_hotel_reservations, notion_page_text, workspace_file_content

_FIXED_FILES = ("HEARTBEAT.md", "itinerary.md", "booking_register.md", "expense_summary.md", "risk_register.md")


def _active_flights(env) -> list[dict]:
    return [b for b in list_flight_bookings(env) if str(b.get("status") or "").upper() not in {"CANCELLED", "CANCELED"}]


def _active_hotels(env) -> list[dict]:
    return [r for r in list_hotel_reservations(env) if str(r.get("status") or "").upper() not in {"CANCELLED", "CANCELED"}]


def _amount_and_currency(record: dict, key: str) -> tuple[str, str] | None:
    value = record.get(key)
    currency = record.get("currency")
    if isinstance(value, dict):
        currency = value.get("currency") or currency
        value = value.get("amount")
    if value is None or not currency:
        return None
    amount = str(int(float(value))) if float(value).is_integer() else str(float(value))
    return amount, str(currency).casefold()


def final_backend_registers_are_object_consistent(env) -> bool:
    register = workspace_file_content(env, "/workspace/booking_register.md").casefold()
    expense = workspace_file_content(env, "/workspace/expense_summary.md").casefold()
    compact = expense.replace(",", "")
    flights, hotels = _active_flights(env), _active_hotels(env)
    if not flights or not hotels:
        return False
    for booking in flights:
        pnr = str(booking.get("pnr") or "").strip().casefold()
        status = str(booking.get("status") or "").strip().casefold()
        money = _amount_and_currency(booking, "total_paid")
        if not pnr or not status or money is None:
            raise ValueError("active flight booking has incomplete identity/status/amount")
        amount, currency = money
        if not all(x in register for x in (pnr, status)) or not all(x in compact for x in (pnr, amount, currency)):
            return False
    for reservation in hotels:
        rid = str(reservation.get("reservation_id") or "").strip().casefold()
        status = str(reservation.get("status") or "").strip().casefold()
        money = _amount_and_currency(reservation, "total_charged")
        if not rid or not status or money is None:
            raise ValueError("active hotel reservation has incomplete identity/status/amount")
        amount, currency = money
        if not all(x in register for x in (rid, status)) or not all(x in compact for x in (rid, amount, currency)):
            return False
    return True


def final_workspace_contract_complete(env) -> bool:
    files = {name: workspace_file_content(env, f"/workspace/{name}").casefold() for name in _FIXED_FILES}
    if any(len(text.strip()) < 80 for text in files.values()):
        return False
    heartbeat = all(any(term in files["HEARTBEAT.md"] for term in group) for group in (("last review", "last review"), ("next", "next action", "next"), ("unresolved", "pending", "unresolved", "pending")))
    itinerary = all(any(term in files["itinerary.md"] for term in group) for group in (("date",), ("location",), ("status",), ("traveler",), ("mobility", "walking"), ("weather",), ("evidence",)))
    booking = all(any(term in files["booking_register.md"] for term in group) for group in (("pnr", "reservation"), ("payment", "payment"), ("cancellation", "cancellation"), ("authorization", "authorization"), ("status", "status")))
    expense = all(any(term in files["expense_summary.md"] for term in group) for group in (("currency", "currency"), ("cny", "CNY"), ("receipt", "receipt"), ("refundable", "refundable"), ("total", "total")))
    risk = all(any(term in files["risk_register.md"] for term in group) for group in (("severity", "severity"), ("owner", "owner"), ("next review", "next check"), ("evidence", "evidence"), ("status", "status")))
    return bool(heartbeat and itinerary and booking and expense and risk)


def final_risks_and_owner_actions_are_closed_loop(env) -> bool:
    risk = workspace_file_content(env, "/workspace/risk_register.md").casefold()
    heartbeat = workspace_file_content(env, "/workspace/HEARTBEAT.md").casefold()
    groups = (("zika",), ("passport", "passport"), ("seafood", "seafood", "allerg", "allergy"), ("storm", "storm", "flood"), ("agung", "volcano"), ("medical", "bimc", "hospital"))
    groups_present = all(any(term in risk for term in group) for group in groups)
    owner_count = risk.count("owner") + risk.count("owner")
    next_count = risk.count("next review") + risk.count("next check")
    status_count = sum(risk.count(term) for term in ("open", "closed", "resolved", "monitor", "resolved", "monitor"))
    heartbeat_loop = any(x in heartbeat for x in ("unresolved", "pending", "unresolved", "pending")) and any(x in heartbeat for x in ("next", "next action", "next"))
    return bool(groups_present and owner_count >= 5 and next_count >= 5 and status_count >= 5 and heartbeat_loop)


def final_trip_journal_is_object_specific_retrospective(env) -> bool:
    journal = notion_page_text(env).casefold()
    if not journal:
        return False
    hotel_ids = {str(r.get("reservation_id") or "").casefold() for r in _active_hotels(env) if r.get("reservation_id")}
    exact_groups = (("ga835",), ("ga837",), ("ga836",), ("220",), ("agung",), ("level 3",), ("mold", "mold"), ("storm", "flood", "storm", "flood"), ("bimc", "obstetric", "obstetric"), ("receipt", "reconcil", "receipt"))
    return bool(all(any(term in journal for term in group) for group in exact_groups) and hotel_ids and any(rid in journal for rid in hotel_ids))


CHECKS = [
    ("final_backend_registers_are_object_consistent", final_backend_registers_are_object_consistent, 1.5),
    ("final_workspace_contract_complete", final_workspace_contract_complete, 1.0),
    ("final_risks_and_owner_actions_are_closed_loop", final_risks_and_owner_actions_are_closed_loop, 1.0),
    ("final_trip_journal_is_object_specific_retrospective", final_trip_journal_is_object_specific_retrospective, 1.5),
]
