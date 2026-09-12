"""Stage 17 rubric — Shinkansen suspension + hypoglycemia event (D17)."""
from __future__ import annotations


from .shared._helpers import _all_corpus
from .cross_stage import shinkansen_alt_with_notion_decision

from loguru import logger


def s17_shinkansen_alt_route(env) -> bool:
    """Agent proposes an alternative for the JR suspension window."""
    corpus = _all_corpus(env)
    if not corpus.strip():
        logger.info("s17 alt route: no state; FAIL (required state unavailable)")
        return False
    alt_cues = ["later train", "15:00", "reschedule", "alternate",
                "alt route", "limited express", "thunderbird", "haruka",
                "bus", "taxi", "rental car", "nozomi", "hikari",
                "after 15", "afternoon departure", "kodama", "shin-osaka"]
    hits = sum(1 for c in alt_cues if c in corpus)
    ok = hits >= 2
    logger.info(f"s17 alt route: hits={hits} {'PASS' if ok else 'FAIL'}")
    return ok


def s17_hypoglycemia_triage(env) -> bool:
    """Hypo event: ≥2 of (clinic, insurance claim, followup/monitor)."""
    corpus = _all_corpus(env)
    if not corpus.strip():
        logger.info("s17 hypo: no state; FAIL (required state unavailable)")
        return False
    clinic = any(k in corpus for k in ["clinic", "hospital"])
    insurance = any(k in corpus for k in ["insurance", "claim",
                                          "allianz", "ti-q-88231"])
    followup = any(k in corpus for k in ["follow up", "followup", "check back",
                                          "rest", "hydrate", "monitor",
                                          "blood sugar", "glucose"])
    score = clinic + insurance + followup
    ok = score >= 2
    logger.info(f"s17 hypo: clinic={clinic} ins={insurance} follow={followup} {'PASS' if ok else 'FAIL'}")
    return ok


CHECKS = [
    ("s17_shinkansen_alt_route",              s17_shinkansen_alt_route,            2),
    ("s17_hypoglycemia_triage",               s17_hypoglycemia_triage,             3),
    ("d_shinkansen_alt_with_notion_decision", shinkansen_alt_with_notion_decision, 2),
]
