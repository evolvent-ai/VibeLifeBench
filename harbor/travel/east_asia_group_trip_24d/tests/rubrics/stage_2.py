"""Stage 2: exact three-leg searches plus a traveler-specific option register."""
from __future__ import annotations

from loguru import logger

from ._helpers import _tool_calls, _tool_name_matches, _workspace_file_text


def _route_call(args: dict, origins: set[str], destinations: set[str], date: str, adults: int) -> bool:
    return (
        str(args.get("origin") or "").upper() in origins
        and str(args.get("destination") or "").upper() in destinations
        and str(args.get("departure_date") or "") == date
        and int(args.get("adults") or 0) == adults
    )


def s2_exact_three_leg_searches(env) -> bool:
    calls = [
        call.get("arguments")
        for call in _tool_calls(env, 2)
        if _tool_name_matches(str(call.get("name") or ""), "flight_booking", "search_flights")
        and isinstance(call.get("arguments"), dict)
    ]
    outbound = any(_route_call(a, {"PVG", "SHA"}, {"NRT", "HND"}, "2026-06-05", 4) for a in calls)
    tokyo_seoul = any(_route_call(a, {"NRT", "HND"}, {"ICN", "GMP"}, "2026-06-08", 3) for a in calls)
    return_leg = any(_route_call(a, {"ICN", "GMP"}, {"PVG", "SHA"}, "2026-06-10", 3) for a in calls)
    result = outbound and tokyo_seoul and return_leg
    logger.info("s2_exact_three_leg_searches: {}", "PASS" if result else "FAIL")
    return result


def s2_flight_options_are_durable_and_traveler_specific(env) -> bool:
    text = _workspace_file_text(env, "/workspace/flights.md").lower()
    routes = all(
        all(token in text for token in tokens)
        for tokens in (("2026-06-05", "pvg", "nrt"), ("2026-06-08", "nrt", "icn"), ("2026-06-10", "icn", "pvg"))
    )
    zhao = "zhao min" in text and "seoul" in text and any(
        x in text for x in ("does not travel", "does not join", "only tokyo", "skip")
    )
    option_state = any(x in text for x in ("option", "candidate")) and any(
        x in text for x in ("price", "fare")
    )
    result = bool(routes and zhao and option_state)
    logger.info("s2_flight_options_are_durable_and_traveler_specific: {}", "PASS" if result else "FAIL")
    return result


CHECKS = [
    ("s2_exact_three_leg_searches", s2_exact_three_leg_searches, 1.0),
    ("s2_flight_options_are_durable_and_traveler_specific", s2_flight_options_are_durable_and_traveler_specific, 1.0),
]
