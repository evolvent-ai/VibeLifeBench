"""Stage 7 rubric — insulin guidance + doctor-letter todo (D7)."""
from __future__ import annotations


from .shared._helpers import (
    _all_corpus,
    _any_kw,
    _cron_reminders,
    _emails_for,
    _notion_body,
)
from .cross_stage import hotel_minifridge_insulin, mother_raw_fish_avoid

from loguru import logger


_INSULIN_POINTS = [
    ("carryon", ["carry-on", "carry on", "hand luggage"]),
    ("doctor_letter", ["doctor", "letter", "medical", "prescription"]),
    ("customs", ["customs", "declare", "declaration", "disclosure"]),
    ("supply_qty", ["supply", "30 day", "20 day", "quantity", "amount", "backup", "spare"]),
]


def s7_insulin_guidance(env) -> bool:
    """Agent-authored durable state covers at least three insulin-preparation facets."""
    durable = _all_corpus(env)
    covered = {name for name, terms in _INSULIN_POINTS if _any_kw(durable, terms)}
    ok = len(covered) >= 3
    logger.info(f"s7 insulin: covered={sorted(covered)} -> {ok}")
    return bool(ok)


def s7_doctor_letter_todo(env) -> bool:
    """Notion todo / cron reminder for the doctor's letter."""
    terms = ["doctor", "letter", "prescription"]
    for r in _cron_reminders(env):
        if _any_kw(r.get("text") or "", terms):
            logger.info("s7 doctor letter: PASS via cron reminder")
            return True
    body = _all_corpus(env)
    if body and _any_kw(body, terms):
        logger.info("s7 doctor letter: PASS via notion journal")
        return True
    logger.info("s7 doctor letter: FAIL")
    return False


CHECKS = [
    ("s7_insulin_guidance",        s7_insulin_guidance,        2),
    ("s7_doctor_letter_todo",      s7_doctor_letter_todo,      1),
    ("d_mother_raw_fish_avoid",    mother_raw_fish_avoid,      0.5),
    ("d_hotel_minifridge_insulin", hotel_minifridge_insulin,   0.5),
]
