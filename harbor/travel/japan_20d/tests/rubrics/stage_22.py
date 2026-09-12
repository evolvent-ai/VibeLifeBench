"""Stage 22 rubric — return-flight check-in opens (D22)."""
from __future__ import annotations


from .shared._helpers import _all_corpus, _call
from .cross_stage import unionpay_kix_nrt_cash

from loguru import logger


def s22_return_checkin(env) -> bool:
    """Return-flight online check-in opened; agent completed it."""
    bookings = _call(env, "flight_booking", "list_bookings", user_id="li_wei")
    checked = False
    if isinstance(bookings, dict):
        pnrs = [b.get("pnr") for b in bookings.get("bookings", []) or []]
        for pnr in pnrs:
            if not pnr:
                continue
            b = _call(env, "flight_booking", "get_booking", pnr=pnr)
            if not isinstance(b, dict):
                continue
            hist = b.get("history") or []
            if any("check_in" in (h.get("event", "") or "").lower()
                   or "CHECK_IN" in (h.get("event", "") or "")
                   for h in hist):
                checked = True
                break
            for seg in b.get("segments", []) or []:
                if (seg.get("flight_no") or "").upper() in ("MU550", "JL551"):
                    for s in seg.get("seats", []) or []:
                        if s.get("boarding_pass_id"):
                            checked = True
                            break

    if checked:
        logger.info("s22 checkin: flight DB confirms check-in; PASS")
        return True

    corpus = _all_corpus(env)
    if not corpus.strip():
        logger.info("s22 checkin: no state; FAIL (required state unavailable)")
        return False
    cues = ["check-in", "checked in", "boarding pass", "mu550",
            "return flight", "online check"]
    hits = sum(1 for c in cues if c in corpus)
    ok = hits >= 1
    logger.info(f"s22 checkin: hits={hits} {'PASS' if ok else 'FAIL'}")
    return ok


CHECKS = [
    ("s22_return_checkin",     s22_return_checkin,    1),
    ("d_unionpay_kix_nrt_cash", unionpay_kix_nrt_cash, 0.5),
]
