"""Stage 15 rubric — first full day in Tokyo, walking + meal cadence (D15)."""
from __future__ import annotations

from datetime import datetime
import re

from .shared._helpers import (
    _all_corpus,
    _all_calendar_events,
    _any_kw,
)

from loguru import logger


_DISTANCE_PATTERN = re.compile(r"(\d+(?:\.\d+)?)\s*(?:km|kilometers?)",
                                re.IGNORECASE)
# The cap is a *per-day* walking budget, so only distances expressed as a
# daily budget ("<n> km per day", "<n> km/day", ...) may fail the check.
# Incidental distances (a 60 km airport transfer, a 0.9 km hotel walk) are
# contextual and must not fail the day-plan check.
_PER_DAY_BUDGET = re.compile(
    r"(\d+(?:\.\d+)?)\s*(?:km|kilometers?)\s*"
    r"(?:per day|/day|a day|daily|per-day)",
    re.IGNORECASE)
# Walk-adjacent distances satisfy "numeric walking load present" but can
# never exceed the cap on their own (no per-day framing).
_WALK_ADJACENT = re.compile(
    r"(?:walk(?:ing)?|stroll|on foot|pace|mobility)[^.\n]{0,40}?"
    r"(\d+(?:\.\d+)?)\s*(?:km|kilometers?)",
    re.IGNORECASE)


def _walking_distances(text: str) -> list[float]:
    budgets = [float(m.group(1)) for m in _PER_DAY_BUDGET.finditer(text)]
    if budgets:
        return budgets
    return [d for d in (float(m.group(1))
                        for m in _WALK_ADJACENT.finditer(text))
            if d <= 4.0]


def s15_itinerary_adjust_walking(env) -> bool:
    """Day plan respects father's ≤4 km/day walking cap."""
    text = _all_corpus(env)
    if not text:
        logger.info("s15 walking: notion empty → True (lenient)")
        return False
    if not _any_kw(text, ["walking", "walk", "km", "kilometer"]):
        logger.info("s15 walking: no walking mention → False")
        return False
    distances = _walking_distances(text)
    if not distances:
        logger.info("s15 walking: no numeric walking load -> False")
        return False
    if any(d > 4.0 for d in distances):
        logger.info(f"s15 walking: distance > 4km found ({[d for d in distances if d > 4.0]}) → False")
        return False
    logger.info(f"s15 walking: distances={distances} ≤ 4km → True")
    return True


_TIME_TOKEN = re.compile(r"\b([01]?\d|2[0-3]):([0-5]\d)\b")
_MEAL_WORDS = [
    "breakfast", "lunch", "dinner", "brunch", "snack",
]
_MEAL_TOKEN = r"(?:breakfast|lunch|dinner|brunch|snack)"
_CLOCK_TOKEN = r"(?P<hour>[01]?\d|2[0-3]):(?P<minute>[0-5]\d)"
_MEAL_THEN_TIME = re.compile(
    rf"\b{_MEAL_TOKEN}\b[^0-9\n]{{0,32}}{_CLOCK_TOKEN}", re.IGNORECASE
)
_TIME_THEN_MEAL = re.compile(
    rf"{_CLOCK_TOKEN}[^,;\n]{{0,32}}\b{_MEAL_TOKEN}\b", re.IGNORECASE
)
_MEAL_PLAN_DATE = "2026-05-02"


def s15_meal_gap_diabetes(env) -> bool:
    """Meal times must not have >3h gaps — hypoglycemia risk."""
    def _scan_times(blob: str) -> list[int]:
        out: set[int] = set()
        for line in blob.splitlines():
            for pattern in (_MEAL_THEN_TIME, _TIME_THEN_MEAL):
                for match in pattern.finditer(line):
                    out.add(
                        int(match.group("hour")) * 60 + int(match.group("minute"))
                    )
        return sorted(out)

    any_meal_signal = False
    times: list[int] = []

    text = _all_corpus(env)
    if text:
        t = _scan_times(text)
        if any(w in text.lower() for w in _MEAL_WORDS):
            any_meal_signal = True
        times.extend(t)

    for e in _all_calendar_events(env) or []:
        blob = (str(e.get("summary") or "") + " "
                + str(e.get("description") or ""))
        low = blob.lower()
        if not any(w in low for w in _MEAL_WORDS):
            continue
        start = e.get("start")
        raw_start = start.get("dateTime") if isinstance(start, dict) else None
        if not isinstance(raw_start, str):
            continue
        try:
            local_start = datetime.fromisoformat(raw_start.replace("Z", "+00:00"))
        except ValueError:
            continue
        if local_start.date().isoformat() != _MEAL_PLAN_DATE:
            continue
        any_meal_signal = True
        times.append(local_start.hour * 60 + local_start.minute)

    if not any_meal_signal:
        logger.info("s15 meal gap: NO meal signal → False (safety-critical fail-closed)")
        return False

    if len(times) < 2:
        logger.info("s15 meal gap: signal present but <2 times parsed → False")
        return False
    times = sorted(set(times))
    gaps = [b - a for a, b in zip(times, times[1:])]
    worst = max(gaps)
    ok = worst <= 180
    logger.info(f"s15 meal gap: times={times} gaps={gaps} worst={worst} → {ok}")
    return ok


CHECKS = [
    ("s15_itinerary_adjust_walking", s15_itinerary_adjust_walking, 1.5),
    ("s15_meal_gap_diabetes",        s15_meal_gap_diabetes,        1.5),
]
