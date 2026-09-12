"""Stage 2 rubric — flight equipment swap + first-international (D2)."""
from __future__ import annotations


from .shared._helpers import _call, _list_flight_bookings
from .cross_stage import first_international_explain

from loguru import logger


def s2_seat_reselect(env) -> bool:
    """Agent reselected seats after the MU549 equipment swap."""
    bookings = _list_flight_bookings(env)
    if not bookings:
        logger.info("s2 seat: lenient pass — no booking yet")
        return False
    for b in bookings:
        pnr = b.get("pnr")
        if not pnr:
            continue
        detail = _call(env, "flight_booking", "get_booking", pnr=pnr)
        if not isinstance(detail, dict):
            continue
        for h in detail.get("history") or []:
            evt = (h.get("event") or "").lower()
            det = (h.get("detail") or "").lower()
            if "change" in evt or "seat" in evt or "seat" in det:
                logger.info(f"s2 seat: PASS via history on PNR {pnr}")
                return True
        for seg in (detail.get("segments") or []):
            if seg.get("flight_no") == "MU549":
                seats = seg.get("seats") or []
                if seats:
                    logger.info("s2 seat: PASS via populated seats on MU549")
                    return True
    logger.info("s2 seat: FAIL — no evidence of reselect")
    return False


CHECKS = [
    ("s2_seat_reselect",              s2_seat_reselect,              1.5),
    ("d_first_international_explain", first_international_explain,   0.5),
]
