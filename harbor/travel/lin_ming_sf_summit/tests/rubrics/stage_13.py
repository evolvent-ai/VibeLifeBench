"""Stage 13: notification — hotel prices surged."""
from __future__ import annotations
from loguru import logger
from ._helpers import _tool_called_in_stage, _tool_with_args, _ws, _stage_text, _stage_tools, _trace_successful


def s13_hotel_surge_handled(env) -> bool:
    """Stage 13 called search_hotels / get_hotel for San Francisco AND agent response or budget_tracker.md mentions price surge/surge/price increase."""
    ok_tools = False
    for tc in _stage_tools(env, 13):
        if not _trace_successful(tc):
            continue
        name = (tc.get("name") or "").lower()
        if "search_hotels" in name or "get_hotel" in name:
            args = tc.get("arguments") or {}
            arg_str = str(args).lower()
            if "san francisco" in arg_str or "sf" in arg_str or "San Francisco" in arg_str:
                ok_tools = True
                break
    text = _stage_text(env, 13).lower()
    budget = _ws(env, "/workspace/budget_tracker.md").lower()
    combined = text + "\n" + budget
    ok_text = any(w in combined for w in ["price surge", "surge", "price increase", "increase", "increased", "price change", "more expensive", "surge amount"])
    ok_decision = any(w in combined for w in [
        "alternative", "confirm booking", "change hotel", "control budget", "reassess",
        "value", "compare", "compare", "search again", "search again", "review again", "alternative", "budget", "cheaper",
    ])
    ok = ok_tools and ok_text and ok_decision
    logger.info(f"s13_hotel_surge_handled: tools={ok_tools} text={ok_text} decision={ok_decision} -> {ok}")
    return ok


CHECKS = [
    ("s13_hotel_surge_handled", s13_hotel_surge_handled, 1.25),
]
