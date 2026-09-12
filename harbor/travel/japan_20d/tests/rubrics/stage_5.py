"""Stage 5 rubric — insurance quote + flight-search tool-use gate (D5)."""
from __future__ import annotations


from .shared._helpers import (
    _all_corpus,
    _any_kw,
    _cron_reminders,
    _list_flight_bookings,
    _sent_emails_any,
)

from loguru import logger


def s5_insurance_quote_action(env) -> bool:
    """Agent responded to the Allianz quote."""
    markers = ["allianz", "ti-q-88231", "insurance"]
    body = _all_corpus(env)
    if body and _any_kw(body, markers):
        logger.info("s5 insurance: PASS via notion")
        return True
    for r in _cron_reminders(env):
        if _any_kw(r.get("text") or "", markers):
            logger.info("s5 insurance: PASS via cron")
            return True
    msgs = _sent_emails_any(env)
    for m in msgs:
        blob = str(m.get("subject") or "") + "\n" + str(m.get("body") or "")
        if _any_kw(blob, markers):
            logger.info("s5 insurance: PASS via email")
            return True
    logger.info("s5 insurance: FAIL")
    return False


def flight_search_called(env) -> bool:
    """By end of stage 5, flight_booking.search_flights must have been invoked."""
    bookings = _list_flight_bookings(env)
    if bookings:
        logger.info(f"s0-5 tool-use: PASS via {len(bookings)} booking(s)")
        return True
    logger.info("s0-5 booking: FAIL — zero persisted bookings")
    return False


CHECKS = [
    ("s5_insurance_quote_action", s5_insurance_quote_action, 1),
    ("s5_flight_booked",          flight_search_called,      1.5),
]
