"""Stage 9: departure - route query from Narita Airport to the hotel."""
from __future__ import annotations
from loguru import logger
from ._helpers import _any, _stage_corpus, _agent_used_tool, _workspace_file_text


def s9_arrival_guidance(env) -> bool:
    """Agent provided route from NRT to Roppongi hotel."""
    text = _stage_corpus(env, 9) + "\n" + _workspace_file_text(env, "/workspace/itinerary.md").lower()
    checked_route = _agent_used_tool(env, "maps", "directions", stage=9) or _agent_used_tool(env, "maps", "get_transit", stage=9)
    has_route = _any(text, ["narita"]) and _any(text, ["roppongi"])
    has_mode = _any(text, ["narita express", "skyliner", "keisei", "bus", "limousine", "subway"])
    has_operational_detail = _any(text, ["minutes", "min", "transfer", "cost", "jpy", "station"])
    persisted = "itinerary" in text or _any(_workspace_file_text(env, "/workspace/itinerary.md").lower(), ["narita"])
    ok = checked_route and has_route and has_mode and has_operational_detail and persisted
    logger.info(f"s9_arrival: route_call={checked_route} route={has_route} mode={has_mode} detail={has_operational_detail} persisted={persisted} -> {'PASS' if ok else 'FAIL'}")
    return ok


CHECKS = [
    ("s9_arrival_guidance", s9_arrival_guidance, 1.5),
]
