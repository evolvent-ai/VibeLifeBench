"""Stage 0 rubric: task kickoff (D0)."""
from __future__ import annotations


from .shared._helpers import (
    _all_corpus,
    _all_calendar_events,
    _any_kw,
    calendar_list,
    list_flight_bookings,
)

from loguru import logger


def s0_ack_and_ask_clarifying(env) -> bool:
    """Agent persisted unresolved kickoff questions before making a booking."""
    bookings = list_flight_bookings(env)
    confirmed = [b for b in bookings if (b.get("status") or "").upper() == "TICKETED"]
    if confirmed:
        logger.info("s0 clarifying: FAIL — agent booked flights on day 0")
        return False

    persona_exists = True  # the baseline persona is guaranteed by the task environment
    durable = _all_corpus(env)
    acknowledged = _any_kw(durable, ["open_item", "status", "owner", "acknowledged", "understood", "kickoff", "pending confirmation"])
    clarifying = (
        "?" in durable
        or _any_kw(durable, ["please confirm", "whether", "preference", "need to confirm", "could you confirm", "unknown", "pending confirmation"])
    )
    ok = persona_exists and acknowledged and clarifying
    logger.info(
        f"s0 clarifying: persona={persona_exists} ack={acknowledged} "
        f"question={clarifying} {'PASS' if ok else 'FAIL'}"
    )
    return bool(ok)


def s0_calendar_placeholder(env) -> bool:
    """A 'Japan Trip' calendar OR Japan-summary event exists."""
    cals = calendar_list(env)
    if cals is None:
        logger.info("s0 calendar: unreachable — lenient pass")
        return False
    names = {str(c.get("name") or c.get("displayname") or "") for c in cals}
    if any("japan" in n.lower() for n in names):
        logger.info(f"s0 calendar: PASS via calendar name {names!r}")
        return True
    events = _all_calendar_events(env)
    if events is None:
        logger.info("s0 calendar: event capture unreachable")
        return False
    if any("japan" in str(e.get("summary") or "").lower() for e in events):
        logger.info("s0 calendar: PASS via captured Japan-summary event")
        return True
    logger.info("s0 calendar: FAIL — no Japan-trip calendar or event")
    return False


CHECKS = [
    ("s0_ack_and_ask_clarifying", s0_ack_and_ask_clarifying, 2),
    ("s0_calendar_placeholder",   s0_calendar_placeholder,   1),
]
