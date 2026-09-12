"""Cross-stage checks — verify consistency across the whole task."""
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
    _flatten_text,
    _is_sfo_pek_return,
    _hotel_covers_summit,
    _has_transit_hkg,
    _is_pek_sfo_direct_economy,
    _is_valid_outbound,
    _call,
    _email_has_approval_request,
)


def cross_flight_hotel_date_consistent(env) -> bool:
    """Outbound (3/26-27) + a valid return (3/30-4/10) exist and hotel covers the summit window (3/28-3/30)."""
    bookings = _flight_bookings(env)
    outbound = any(_is_valid_outbound(b) for b in bookings)
    return_flight = any(_is_sfo_pek_return(b) for b in bookings)

    hotels = _hotel_reservations(env)
    hotel_ok = any(_hotel_covers_summit(h) for h in hotels)

    ok = outbound and return_flight and hotel_ok
    logger.info(f"cross_flight_hotel_date_consistent: outbound={outbound} return={return_flight} hotel={hotel_ok} -> {ok}")
    return ok


def cross_budget_booking_consistent(env) -> bool:
    """budget_tracker.md records flight + hotel + a total line, AND backend actually
    has BOTH a flight booking and a hotel reservation (not just one)."""
    bt = _ws(env, "/workspace/budget_tracker.md").lower()
    has_flight = _any(bt, ["flight", "flight", "flight"])
    has_hotel = _any(bt, ["hotel", "hotel"])
    has_total = _any(bt, ["total", "total", "total", "total"])
    has_flight_booking = bool(_flight_bookings(env))
    has_hotel_booking = bool(_hotel_reservations(env))
    ok = has_flight and has_hotel and has_total and has_flight_booking and has_hotel_booking
    logger.info(
        f"cross_budget_booking_consistent: flight_kw={has_flight} hotel_kw={has_hotel} total_kw={has_total} "
        f"flight_booking={has_flight_booking} hotel_booking={has_hotel_booking} -> {ok}"
    )
    return ok


def cross_passport_evus_with_booking(env) -> bool:
    """Passport/EVUS issue documented and backend has bookings."""
    text = _ws(env, "/workspace/trip_plan.md").lower()
    has_passport = _any(text, ["passport", "passport", "2026-05-30", "May 30"])
    has_evus = _any(text, ["evus", "2026-03-25", "March 25"])
    has_booking = bool(_flight_bookings(env) or _hotel_reservations(env))
    ok = (has_passport or has_evus) and has_booking
    logger.info(f"cross_passport_evus_with_booking: passport={has_passport} evus={has_evus} booking={has_booking} -> {ok}")
    return ok


def cross_email_notion_consistent(env) -> bool:
    """Approval email to zhang_manager exists and Notion page has trip content."""
    emails = _sent_emails(env)
    has_email = any(_email_has_approval_request(e) for e in emails)
    notion = _notion_text(env).lower()
    has_notion = bool(notion.strip()) and _any(notion, ["San Francisco", "san francisco", "flight", "flight", "hotel", "hotel"])
    ok = has_email and has_notion
    logger.info(f"cross_email_notion_consistent: email={has_email} notion={has_notion} -> {ok}")
    return ok


def cross_mutation_adaptation(env) -> bool:
    """Final flight state reflects adaptation to the two silent flight disruptions:
    (1) direct PEK-SFO cancelled  -> outbound is a transit booking and no active
        PEK-SFO direct-economy booking remains;
    (2) aircraft changed          -> a seat is assigned on a booking.
    Grounded purely in backend state, so a 'narrating' agent that didn't really
    re-book / re-select cannot pass."""
    bookings = _flight_bookings(env)
    if not bookings:
        logger.info("cross_mutation_adaptation: no bookings -> False")
        return False
    has_transit = any(_has_transit_hkg(b) for b in bookings)
    no_direct_economy = not any(_is_pek_sfo_direct_economy(b) for b in bookings)
    # Seat assignments are structured under segments[].seats[].seat. Looking
    # only at flattened values loses the ``seat`` key, so a real assignment
    # such as ``12A`` was incorrectly treated as absent.
    has_seat = any(
        any(
            isinstance(segment, dict)
            and any(
                isinstance(seat, dict)
                and bool(str(seat.get("seat") or "").strip())
                for seat in (segment.get("seats") or [])
            )
            for segment in (booking.get("segments") or [])
        )
        for booking in bookings
        if isinstance(booking, dict)
    )
    ok = has_transit and no_direct_economy and has_seat
    logger.info(
        f"cross_mutation_adaptation: transit={has_transit} no_direct_eco={no_direct_economy} seat={has_seat} -> {ok}"
    )
    return ok


CHECKS = [
    ("cross_flight_hotel_date_consistent", cross_flight_hotel_date_consistent, 1.5),
    ("cross_budget_booking_consistent", cross_budget_booking_consistent, 1.5),
    ("cross_passport_evus_with_booking", cross_passport_evus_with_booking, 1.25),
    ("cross_email_notion_consistent", cross_email_notion_consistent, 1.25),
    ("cross_mutation_adaptation", cross_mutation_adaptation, 1.0),
]
