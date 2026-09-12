"""Stage 14 rubric — departure day brief (D14)."""
from __future__ import annotations


from .shared._helpers import _all_corpus, _any_kw
from .cross_stage import timezone_meal_adjust

from loguru import logger


def s14_departure_day_brief(env) -> bool:
    """Morning brief covers flight status + airport transit + blood-sugar."""
    flight_terms = ["mu549", "flight status", "eta", "etd", "gate", "boarding"]
    airport_terms = ["pvg", "nrt", "airport", "transit", "trn"]
    bg_terms = ["blood sugar", "glucose", "insulin", "hypoglycemia", "hypo"]

    text = _all_corpus(env)
    ok = _any_kw(text, flight_terms) and _any_kw(text, airport_terms) and _any_kw(text, bg_terms)
    logger.info(f"s14 brief: durable={bool(text)} -> {ok}")
    return bool(ok)


CHECKS = [
    ("s14_departure_day_brief", s14_departure_day_brief, 1.5),
    ("d_timezone_meal_adjust",  timezone_meal_adjust,    0.5),
]
