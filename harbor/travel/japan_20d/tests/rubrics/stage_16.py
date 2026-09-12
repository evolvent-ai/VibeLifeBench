"""Stage 16 rubric — hotel overbook walk (D16)."""
from __future__ import annotations


from .shared._helpers import _all_corpus, _call
from .cross_stage import hotel_walk_calendar_updated

from loguru import logger


def s16_walk_acceptance(env) -> bool:
    """Agent acknowledged the walk, updated plan, relayed to Li Wei."""
    corpus = _all_corpus(env)
    cues = ["tokyu stay", "walked", "overbook", "taxi voucher", "rebook",
            "granbell", "0.9 km", "0.9km"]
    hits = sum(1 for c in cues if c in corpus)

    walked_in_db = False
    ids_blob = _call(env, "hotel_booking", "list_reservations", user_id="li_wei")
    if isinstance(ids_blob, dict):
        for rid in ids_blob.get("reservation_ids", []) or []:
            r = _call(env, "hotel_booking", "get_reservation",
                      reservation_id=rid)
            if isinstance(r, dict) and r.get("status") == "walked":
                walked_in_db = True
                break

    if not corpus.strip() and not walked_in_db:
        logger.info("s16 walk: no state readable; FAIL (required state unavailable)")
        return False
    if hits >= 2 or (walked_in_db and hits >= 1):
        logger.info(f"s16 walk: hits={hits} walked_in_db={walked_in_db} PASS")
        return True
    logger.info(f"s16 walk: hits={hits} walked_in_db={walked_in_db} FAIL")
    return False


def s16_compensation_logged(env) -> bool:
    """¥8,000 comp landed in an expense-tracking artifact."""
    corpus = _all_corpus(env)
    if not corpus.strip():
        logger.info("s16 comp: no state readable; FAIL (required state unavailable)")
        return False
    has_amount = any(tok in corpus for tok in ["8000", "8,000", "¥8000", "¥8,000"])
    has_context = any(tok in corpus for tok in
                      ["comp", "compensation", "voucher", "refund", "walked"])
    ok = has_amount and has_context
    logger.info(f"s16 comp: amount={has_amount} ctx={has_context} {'PASS' if ok else 'FAIL'}")
    return ok


CHECKS = [
    ("s16_walk_acceptance",           s16_walk_acceptance,          2.5),
    ("s16_compensation_logged",       s16_compensation_logged,      1),
    ("d_hotel_walk_calendar_updated", hotel_walk_calendar_updated,  1.5),
]
