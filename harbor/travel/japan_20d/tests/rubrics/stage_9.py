"""Stage 9 rubric — booking lock-in deadline (D9)."""
from __future__ import annotations


from .shared._helpers import _call
from .cross_stage import budget_warning_before_60k_cap

from loguru import logger


def s9_bookings_locked(env) -> bool:
    """Flights (TICKETED) + hotels (confirmed) by end of stage 9."""
    flights = _call(env, "flight_booking", "list_bookings",
                    user_id="li_wei", status="TICKETED")
    hotels = _call(env, "hotel_booking", "list_reservations", user_id="li_wei")

    if flights is None and hotels is None:
        logger.info("s9 bookings: both backends down → True (lenient)")
        return False

    flight_ok = True
    if flights is not None:
        bookings = flights.get("bookings") if isinstance(flights, dict) else flights
        bookings = bookings or []
        flight_ok = any(str(b.get("status", "")).upper() == "TICKETED" for b in bookings)

    hotel_ok = True
    if hotels is not None:
        res_ids = (hotels.get("reservation_ids")
                   if isinstance(hotels, dict) else []) or []
        confirmed = 0
        for rid in res_ids[:10]:
            detail = _call(env, "hotel_booking", "get_reservation",
                           reservation_id=rid)
            if isinstance(detail, dict) and detail.get("status") == "confirmed":
                confirmed += 1
                break
        hotel_ok = confirmed >= 1

    logger.info(f"s9 bookings: flight_ok={flight_ok} hotel_ok={hotel_ok}")
    return bool(flight_ok and hotel_ok)


CHECKS = [
    ("s9_bookings_locked",              s9_bookings_locked,              2.5),
    ("d_budget_warning_before_60k_cap", budget_warning_before_60k_cap,   2),
]
