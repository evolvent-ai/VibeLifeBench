"""Stage 3 rubric — hotel price drop + budget Q&A (D3)."""
from __future__ import annotations

import re

from .shared._helpers import (
    _all_corpus,
    _any_kw,
    _call,
    _emails_for,
    _workspace_text,
)
from .cross_stage import passport_raised_first_3_stages

from loguru import logger


def s3_budget_answer(env) -> bool:
    """Agent persisted a budget status with a concrete number."""
    number_re = re.compile(r"\d{1,3}(?:[,，]?\d{3})+|\d{2,}")
    budget_markers = ["budget", "remaining", "spent", "cny", "rmb", "¥", "jpy"]

    bits = [_all_corpus(env), _workspace_text(env)]

    artifact_ok: bool | None = None
    for t in bits:
        if not t:
            continue
        if _any_kw(t, budget_markers) and number_re.search(t):
            artifact_ok = True
            break
    if artifact_ok is None:
        res = _call(env, "hotel_booking", "list_reservations", user_id="li_wei")
        if isinstance(res, dict) and (res.get("reservation_ids") or res.get("count")):
            artifact_ok = True
        elif bits or res is not None:
            artifact_ok = False

    if artifact_ok is True:
        logger.info("s3 budget: PASS")
        return True
    logger.info(f"s3 budget: FAIL (artifact={artifact_ok})")
    return False


CHECKS = [
    ("s3_budget_answer",                 s3_budget_answer,                  1),
    ("d_passport_raised_first_3_stages", passport_raised_first_3_stages,    2),
]
