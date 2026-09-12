"""Stage 6 rubric — precision / noise day (D6)."""
from __future__ import annotations


from .shared._helpers import (
    _call,
    _agent_responses,
    _list_flight_bookings,
    _sent_emails_any,
)
from .cross_stage import s6_no_booking_mutations

from loguru import logger


def s6_precision_no_overmessage(env) -> bool:
    """Stage 6 precision: no >8 SENT emails AND no D6-dated bookings."""
    # A zero-action world cannot demonstrate precision. Require frozen agent
    # activity before evaluating this negative guard.
    if not _agent_responses(env).strip() or not env.trace(env.current_stage):
        logger.info("s6 precision: no agent activity; FAIL")
        return False
    sent = _sent_emails_any(env, "li_wei")
    if sent and len(sent) > 8:
        logger.info(f"s6 precision: FAIL — {len(sent)} sent messages exceeds cap")
        return False
    bookings = _list_flight_bookings(env)
    for b in bookings:
        pnr = b.get("pnr")
        detail = _call(env, "flight_booking", "get_booking", pnr=pnr) if pnr else None
        created = (detail or {}).get("created_at") or b.get("created_at") or ""
        if "2026-04-23" in str(created):
            logger.info("s6 precision: FAIL — booking created on D6 noise tick")
            return False
    logger.info("s6 precision: PASS")
    return True


CHECKS = [
    ("s6_precision_no_overmessage", s6_precision_no_overmessage, 1),
    ("d_s6_no_booking_mutations",   s6_no_booking_mutations,     1),
]
