"""Stage 25 checker: user asks final summary."""
from __future__ import annotations

from loguru import logger

from ._helpers import (
    _stage_text,
    _flight_bookings,
    _hotel_reservations,
    _calendar_events,
    _transactions,
    _any,
)


def s25_summary_consistent(env) -> bool:
    """Agent's summary mentions flight, hotel, calendar, and expenses consistently with backend state."""
    text = _stage_text(env, 25)

    # Backend state checks
    flights = _flight_bookings(env)
    hotels = _hotel_reservations(env)
    events = _calendar_events(env, "2026-03-15T00:00:00", "2026-04-10T23:59:59")
    txs = _transactions(env)

    backend_ok = (
        len(flights) >= 2
        and len(hotels) >= 1
        and len(events) >= 4
    )

    # Agent response mentions the key categories
    mentions_flight = _any(text, ["flight", "flight", "flight", "booking"])
    mentions_hotel = _any(text, ["hotel", "hotel", "accommodation"])
    mentions_calendar = _any(text, ["calendar", "meeting", "calendar", "event", "itinerary"])
    mentions_expense = _any(text, ["cost", "expense", "travel expense", "budget", "spending", "reimbursement", "expense", "cost"])

    categories_ok = mentions_flight and mentions_hotel and mentions_calendar and mentions_expense

    # No false claims: if backend has no flights, agent should not claim there are flights
    # (This is a lightweight check; we mainly verify positive mentions align.)
    ok = backend_ok and categories_ok
    logger.info(
        f"s25_summary_consistent: backend_ok={backend_ok} "
        f"(flights={len(flights)}, hotels={len(hotels)}, events={len(events)}), "
        f"categories_ok={categories_ok} "
        f"(flight={mentions_flight}, hotel={mentions_hotel}, calendar={mentions_calendar}, expense={mentions_expense})"
    )
    return ok


CHECKS = [
    ("s25_summary_consistent", s25_summary_consistent, 1.5),
]
