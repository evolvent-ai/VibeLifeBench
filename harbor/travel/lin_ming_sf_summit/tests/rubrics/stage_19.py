"""Stage 19 checker: world event — SFO wind warning."""
from __future__ import annotations
from loguru import logger
from ._helpers import _tool_called_in_stage, _ws, _any


def s19_return_wind_handled(env) -> bool:
    """Stage 19 checked return flight AND documented wind risk AND provided a contingency plan."""
    ok_tools = _tool_called_in_stage(env, 19, ["get_flight_offer", "get_booking", "get_flight_status", "list_bookings"])  # real flight tools (was phantom get_flight)

    tp = _ws(env, "/workspace/trip_plan.md")
    dl = _ws(env, "/workspace/decision_log.md")
    text = (tp or "") + "\n" + (dl or "")
    has_weather = _any(text, ["high wind", "strong wind", "weather", "advisory", "wind", "weather", "warning", "gust"])
    has_flight = _any(text, ["flight", "return flight", "SFO", "sfo", "return", "flight", "airport", "San Francisco"])
    has_contingency = _any(
        text,
        ["buffer", "early", "delay", "change flight", "change flight", "alternative", "contingency plan", "reserve", "monitor updates", "rebook", "adjustment"],
    )
    ok = ok_tools and has_weather and has_flight and has_contingency
    logger.info(f"s19_return_wind_handled: tools={ok_tools} weather={has_weather} flight={has_flight} contingency={has_contingency} -> {ok}")
    return ok


CHECKS = [
    ("s19_return_wind_handled", s19_return_wind_handled, 1.25),
]
