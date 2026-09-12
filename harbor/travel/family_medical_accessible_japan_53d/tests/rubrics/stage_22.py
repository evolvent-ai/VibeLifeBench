from __future__ import annotations

from ._helpers import (
    _call_json,
    _flight_booking_details,
    _hotel_reservation_details,
    _tool_call_matches,
    _tool_call_results,
    _workspace_file_text,
    text_has,
)

MID = "<kansai-confirm-20261011@kansai-travel.example>"


def _confirmation_row(env) -> dict | None:
    data = _call_json(
        env,
        "email",
        "search_emails",
        query="MU737",
        folder="INBOX",
        page=1,
        page_size=20,
    )
    rows = data.get("emails") or [] if isinstance(data, dict) else []
    return next((row for row in rows if isinstance(row, dict) and row.get("message_id") == MID), None)


def s22_reads_exact_confirmation_email(env) -> bool:
    row = _confirmation_row(env)
    if not row or not row.get("email_id") or not row.get("is_read"):
        return False
    email_id = str(row["email_id"])
    searched = _tool_call_matches(
        env,
        ["email__search_emails"],
        lambda a: any(word in str(a.get("query") or "").lower() for word in ("mu737", "flight", "confirmation", "insurance")) and str(a.get("folder") or "").upper() == "INBOX",
        stage=22,
    )
    read_exact = _tool_call_matches(
        env,
        ["email__read_email"],
        lambda a: str(a.get("email_id") or "") == email_id,
        stage=22,
    )
    return bool(searched and read_exact)


def s22_backend_confirmations_linked(env) -> bool:
    flights = [d for d in _flight_booking_details(env, status="TICKETED") if d.get("status") == "TICKETED"]
    hotels = _hotel_reservation_details(env)
    text = _workspace_file_text(env, "booking_register.md")
    if len(flights) != 1 or not hotels:
        return False
    flight = flights[0]
    if str(flight.get("pnr") or "").lower() not in text:
        return False
    if not any(s.get("flight_no") == "MU737" for s in flight.get("segments") or []):
        return False
    for hotel in hotels:
        rid = str(hotel.get("reservation_id") or "").lower()
        status = str(hotel.get("status") or "").lower()
        deadline = str(hotel.get("refundable_until") or "").lower()
        if not rid or rid not in text or not status or status not in text:
            return False
        if deadline and deadline not in text:
            return False
    return text_has(text, [[MID], ["ins-kansai-2026-381"], ["2026-10-11t18:00"]])


def s22_calendar_has_exact_mu737_event(env) -> bool:
    results = _tool_call_results(
        env,
        ["calendar__create_event"],
        lambda a: "mu737" in str(a.get("summary") or "").lower()
        and str(a.get("start") or "").startswith("2026-10-12T10:00")
        and str(a.get("end") or "").startswith("2026-10-12T13:30"),
        stage=22,
    )
    for row in results:
        if not isinstance(row, dict):
            continue
        start = row.get("start")
        start = start.get("dateTime") if isinstance(start, dict) else start
        end = row.get("end")
        end = end.get("dateTime") if isinstance(end, dict) else end
        blob = (str(row.get("summary") or "") + " " + str(row.get("location") or "") + " " + str(row.get("description") or "")).lower()
        if "mu737" in blob and str(start).startswith("2026-10-12T10:00") and str(end).startswith("2026-10-12T13:30") and "pvg" in blob and "kix" in blob:
            return True
    return False


def s22_workspace_calendar_reference(env) -> bool:
    return text_has(
        _workspace_file_text(env, "trip_plan.md"),
        [["mu737"], ["pvg"], ["kix"], ["2026-10-12t10:00"], ["calendar", "event"]],
    )


CHECKS = [
    ("s22_reads_exact_confirmation_email", s22_reads_exact_confirmation_email, 0.75),
    ("s22_backend_confirmations_linked", s22_backend_confirmations_linked, 1.0),
    ("s22_calendar_has_exact_mu737_event", s22_calendar_has_exact_mu737_event, 0.5),
    ("s22_workspace_calendar_reference", s22_workspace_calendar_reference, 0.5),
]
