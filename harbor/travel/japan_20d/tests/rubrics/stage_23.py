"""Stage 23 rubric — return-flight delay + trip wrap-up (D23)."""
from __future__ import annotations


from .shared._helpers import _all_corpus, _notion_agent_text, _workspace_text
from .cross_stage import flight_delay_communication

from loguru import logger


def s23_delay_lounge_request(env) -> bool:
    """MU550 delay: agent secured lounge access AND meal voucher."""
    corpus = _all_corpus(env)
    if not corpus.strip():
        logger.info("s23 lounge: no state; FAIL (required state unavailable)")
        return False
    has_lounge = any(k in corpus for k in ["sakura lounge", "lounge", "sakura"])
    has_meal = any(k in corpus for k in ["meal voucher", "meal coupon",
                                          "food voucher", "meal"])
    ok = has_lounge and has_meal
    logger.info(f"s23 lounge: lounge={has_lounge} meal={has_meal} {'PASS' if ok else 'FAIL'}")
    return ok


def s23_trip_summary_journal(env) -> bool:
    """Trip-journal has per-day entries. ≥4 distinct trip days referenced."""
    # Seed journal prose is setup, not a trip summary authored by the agent.
    notion = _notion_agent_text(env).lower()
    ws = _workspace_text(env).lower()
    corpus = notion + "\n" + ws
    if not corpus.strip():
        logger.info("s23 journal: no state; FAIL (required state unavailable)")
        return False
    day_tokens = [f"day {i}" for i in range(1, 17)] \
        + [f"d{i}" for i in range(1, 20)] \
        + [f"2026-05-{d:02d}" for d in range(1, 17)]
    hit_days = sum(1 for t in day_tokens if t in corpus)
    city_hits = sum(1 for c in ["tokyo", "kyoto", "osaka", "hakone", "nara"]
                    if c in corpus)
    ok = hit_days >= 4 or (hit_days >= 2 and city_hits >= 3)
    logger.info(f"s23 journal: day_hits={hit_days} city_hits={city_hits} {'PASS' if ok else 'FAIL'}")
    return ok


def s23_expense_reconcile(env) -> bool:
    """Budget tally vs ¥60k — contains budget figure AND tally word."""
    corpus = _all_corpus(env)
    if not corpus.strip():
        logger.info("s23 expense: no state; FAIL (required state unavailable)")
        return False
    has_budget = any(tok in corpus for tok in ["60000", "60,000", "¥60",
                                                "60k", "60000cny", "60000 cny"])
    has_tally = any(tok in corpus for tok in ["total", "sum", "balance",
                                               "under budget", "over budget",
                                               "spent", "remaining",
                                               "reconcile", "expense"])
    ok = has_budget and has_tally
    logger.info(f"s23 expense: budget={has_budget} tally={has_tally} {'PASS' if ok else 'FAIL'}")
    return ok


CHECKS = [
    ("s23_delay_lounge_request",     s23_delay_lounge_request,    1.5),
    ("s23_trip_summary_journal",     s23_trip_summary_journal,    1.5),
    ("s23_expense_reconcile",        s23_expense_reconcile,       1),
    ("d_flight_delay_communication", flight_delay_communication,  1.5),
]
