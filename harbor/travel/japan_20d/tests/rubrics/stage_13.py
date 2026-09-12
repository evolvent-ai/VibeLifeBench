"""Stage 13 rubric — T-1: online check-in + packing list (D13)."""
from __future__ import annotations


from .shared._helpers import _all_corpus, _any_kw, _call

from loguru import logger


def s13_online_checkin(env) -> bool:
    """Agent runs online check-in on T-1. CHECKED_IN entry in booking history."""
    flights = _call(env, "flight_booking", "list_bookings", user_id="li_wei")
    if flights is None:
        logger.info("s13 checkin: flight backend down → True (lenient)")
        return False
    bookings = flights.get("bookings", []) if isinstance(flights, dict) else []
    if not bookings:
        logger.info("s13 checkin: no bookings → False")
        return False
    for b in bookings:
        pnr = b.get("pnr")
        if not pnr:
            continue
        detail = _call(env, "flight_booking", "get_booking", pnr=pnr)
        if not isinstance(detail, dict):
            continue
        hist = detail.get("history") or []
        if any(isinstance(h, dict)
               and str(h.get("event", "")).lower().replace("_", "")
                   in ("checkin", "checkedin")
               for h in hist):
            logger.info(f"s13 checkin: PASS on PNR {pnr}")
            return True
    logger.info("s13 checkin: FAIL")
    return False


def s13_packing_list(env) -> bool:
    """Agent-authored packing checklist includes father's diabetic items."""
    text = _all_corpus(env)
    if not text:
        logger.info("s13 packing: notion empty → True (lenient)")
        return False
    has_packing = _any_kw(text, ["packing", "checklist"])
    diabetic_signals = [
        ["insulin", "insulin-dependent"],
        ["glucose", "glucometer", "strip", "glucose meter", "strips"],
        ["doctor", "letter", "prescription", "doctor's letter", "certificate", "prescription copy"],
        ["glucagon", "rescue"],
    ]
    hits = sum(1 for group in diabetic_signals if _any_kw(text, group))
    ok = has_packing and hits >= 2
    logger.info(f"s13 packing: has_packing={has_packing} diabetic_hits={hits} → {ok}")
    return ok


CHECKS = [
    ("s13_online_checkin", s13_online_checkin, 1.5),
    ("s13_packing_list",   s13_packing_list,   1),
]
