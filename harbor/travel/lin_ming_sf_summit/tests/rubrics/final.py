"""Final checks — grounded in backend state."""
from __future__ import annotations
from loguru import logger
from ._helpers import (
    _flight_bookings,
    _hotel_reservations,
    _calendar_events,
    _transactions,
    _sent_emails,
    _notion_text,
    _ws,
    _any,
    _is_pek_sfo_direct_economy,
    _is_sfo_pek_return,
    _hotel_covers_summit,
    _email_has_approval_request,
    _flatten_text,
    _is_valid_outbound,
)


def final_round_trip_booked(env) -> bool:
    """Backend has both outbound (PEK->SFO direction, 3/26-27) and a valid return (SFO->PEK, 3/30-4/10)."""
    bookings = _flight_bookings(env)
    outbound = False
    return_flight = False
    for b in bookings:
        if _is_valid_outbound(b):
            outbound = True
        if _is_sfo_pek_return(b):
            return_flight = True
    ok = outbound and return_flight
    logger.info(f"final_round_trip: outbound={outbound} return={return_flight} -> {ok}")
    return ok


def final_hotel_booked(env) -> bool:
    """Backend has a San Francisco hotel reservation covering the summit window (3/28-3/30)."""
    hotels = _hotel_reservations(env)
    ok = any(_hotel_covers_summit(h) for h in hotels)
    logger.info(f"final_hotel_booked: {ok}")
    return ok


def final_health_compliant(env) -> bool:
    """A valid outbound exists and no active PEK-SFO direct economy booking exists."""
    bookings = _flight_bookings(env)
    if not bookings:
        logger.info("final_health_compliant: no bookings -> False")
        return False
    violation = any(_is_pek_sfo_direct_economy(b) for b in bookings)
    has_outbound = any(_is_valid_outbound(b) for b in bookings)
    ok = has_outbound and not violation
    logger.info(f"final_health_compliant: outbound={has_outbound} violation={violation} -> {ok}")
    return ok


def final_budget_within_cap(env) -> bool:
    """Active flight and hotel charges, in CNY minor units, stay within the cap."""
    flights = _flight_bookings(env)
    hotels = _hotel_reservations(env)
    flight_amounts = [
        (b.get("total_paid") or {}) for b in flights if _booking_active_for_cost(b)
    ]
    hotel_amounts = [h for h in hotels if _hotel_active_for_cost(h)]
    currencies_ok = all(str(row.get("currency", "")).upper() == "CNY" for row in flight_amounts + hotel_amounts)
    flight_total = sum(float(row.get("amount", 0)) for row in flight_amounts)
    hotel_total = sum(float(row.get("total_charged", 0)) for row in hotel_amounts)
    trip_total = flight_total + hotel_total
    ok = bool(flights and hotels) and currencies_ok and trip_total <= 15000
    logger.info(f"final_budget_within_cap: flights={flight_total} hotels={hotel_total} total={trip_total} currencies={currencies_ok} -> {ok}")
    return ok


def _booking_active_for_cost(booking):
    if str(booking.get("status", "")).lower() in {"cancelled", "canceled", "void", "voided"}:
        return False
    segments = booking.get("segments") if isinstance(booking, dict) else []
    return not any(
        str(segment.get("status", "")).lower() in {"cancelled", "canceled", "void", "voided"}
        for segment in segments if isinstance(segment, dict)
    )


def _hotel_active_for_cost(hotel):
    return str(hotel.get("status", "")).lower() not in {"cancelled", "canceled", "void", "voided"}


def final_approval_email(env) -> bool:
    """Sent folder has an approval-request email to zhang_manager with >5000 amount."""
    emails = _sent_emails(env)
    ok = any(_email_has_approval_request(e) for e in emails)
    logger.info(f"final_approval_email: {ok}")
    return ok


def final_evus_renewal_submitted(env) -> bool:
    """Discoverable EVUS draft reached the public API's submitted/processing state."""
    from ._helpers import _evus_renewal_submitted
    ok = _evus_renewal_submitted(env)
    logger.info(f"final_evus_renewal_submitted: {ok}")
    return ok


def final_passport_remedy(env) -> bool:
    """trip_plan.md documents exact dates, short margin and official confirmation."""
    text = _ws(env, "/workspace/trip_plan.md").lower()
    expiry = _any(text, ["2026-05-30", "05-30", "May 30"])
    trip_end = _any(text, ["2026-03-30", "03-30", "March 30"])
    margin = _any(text, ["short margin", "limited margin", "short margin", "limited margin", "near expiry"])
    confirmation = (
        _any(text, ["carrier", "operating airline", "operating airline", "airline"])
        and _any(text, ["cbp", "official", "CBP", "official"])
        and _any(text, ["confirm", "verify", "written confirmation", "verify", "confirm"])
    )
    contingency = _any(text, ["renew passport", "replace passport", "new passport", "hold booking", "refundable", "refundable", "escalate"])
    ok = expiry and trip_end and margin and confirmation and contingency
    logger.info(
        f"final_passport_remedy: expiry={expiry} trip_end={trip_end} margin={margin} "
        f"confirmation={confirmation} contingency={contingency} -> {ok}"
    )
    return bool(ok)


def final_calendar_complete(env) -> bool:
    """Calendar has >=4 events covering >=3 categories (summit/client visit/standup/flight/hotel/EVUS)."""
    events = _calendar_events(env, "2026-03-15T00:00:00", "2026-04-10T23:59:59")
    if len(events) < 4:
        logger.info(f"final_calendar_complete: count={len(events)} -> False")
        return False
    event_text = _flatten_text(events).lower()
    cats = sum([
        _any(event_text, ["summit", "summit", "moscone"]),
        _any(event_text, ["client visit", "client visit", "downtown"]),
        _any(event_text, ["standup", "stand-up"]),
        _any(event_text, ["flight", "flight", "departure", "arrival", "boarding"]),
        _any(event_text, ["hotel", "hotel", "checkin", "check-out", "check-in"]),
        _any(event_text, ["evus", "visa", "visa", "passport"]),
    ])
    ok = cats >= 3
    logger.info(f"final_calendar_complete: count={len(events)} cats={cats} -> {ok}")
    return ok


def final_notion_archived(env) -> bool:
    """Notion page exists and contains trip + expense info."""
    text = _notion_text(env).lower()
    has_trip = _any(text, ["flight", "flight", "hotel", "hotel", "San Francisco", "san francisco", "summit", "summit"])
    has_expense = _any(text, ["expense", "budget", "reimbursement", "expense", "budget", "reimbursement", "approval"])
    ok = bool(text.strip()) and has_trip and has_expense
    logger.info(f"final_notion_archived: {ok}")
    return ok


CHECKS = [
    ("final_round_trip_booked", final_round_trip_booked, 1.5),
    ("final_hotel_booked", final_hotel_booked, 1.25),
    ("final_health_compliant", final_health_compliant, 2.0),
    ("final_budget_within_cap", final_budget_within_cap, 2.0),
    ("final_approval_email", final_approval_email, 2.0),
    ("final_evus_renewal_submitted", final_evus_renewal_submitted, 1.5),
    ("final_passport_remedy", final_passport_remedy, 1.75),
    ("final_calendar_complete", final_calendar_complete, 1.25),
    ("final_notion_archived", final_notion_archived, 1.0),
]
