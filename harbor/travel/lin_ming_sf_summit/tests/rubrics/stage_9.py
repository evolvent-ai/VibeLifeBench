"""Stage 9: world event — HKG thunderstorm."""
from __future__ import annotations
from loguru import logger
from ._helpers import _tool_called_in_stage, _ws, _any


def s9_transit_weather_handled(env) -> bool:
    """Stage 9 checked transit flights AND documented thunderstorm risk AND provided a contingency plan."""
    ok_tools = _tool_called_in_stage(env, 9, ["get_flight_offer", "get_booking", "list_bookings", "search_flights"])  # real flight tools (was phantom get_flight)
    plan = _ws(env, "/workspace/trip_plan.md").lower()
    dl = _ws(env, "/workspace/decision_log.md").lower()
    text = plan + "\n" + dl

    has_risk = _any(text, ["thunderstorms", "weather", "delay", "advisory", "high wind"])
    has_transit = _any(text, ["Hong Kong", "hkg", "transit", "stopover", "connecting"])
    has_contingency = _any(
        text,
        ["buffer", "early", "delay", "change flight", "change flight", "alternative", "contingency plan", "reserve", "monitor updates", "rebook"],
    )
    ok = ok_tools and has_risk and has_transit and has_contingency
    logger.info(f"s9_transit_weather_handled: tools={ok_tools} risk={has_risk} transit={has_transit} contingency={has_contingency} -> {ok}")
    return ok


CHECKS = [
    ("s9_transit_weather_handled", s9_transit_weather_handled, 1.25),
]
