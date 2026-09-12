"""Stage 3 gate: search Tokyo and Seoul hotels and record cancellation policy."""
from __future__ import annotations

from loguru import logger

from ._helpers import (
    _agent_used_tool,
    _agent_used_any_tool,
    _agent_tool_args_text,
    _workspace_file_text,
    _any,
    _stage_corpus,
)


def s3_gate(env) -> bool:
    """Call search_hotels for both cities and persist candidates and policies."""
    used_search = _agent_used_tool(env, "hotel_booking", "search_hotels", stage=3)

    args = _agent_tool_args_text(env, stage=3)
    has_tokyo = _any(args, ["tokyo", "tyo", "nrt", "shinjuku", "shibuya"])
    has_seoul = _any(args, ["seoul", "sel", "icn", "myeongdong", "hongdae"])
    city_ok = has_tokyo and has_seoul

    # hotels.md must contain candidate hotel information and policy labels.
    hotels_text = _workspace_file_text(env, "/workspace/hotels.md").lower()
    hotels_ok = bool(hotels_text.strip()) and _any(hotels_text, ["hotel", "tokyo", "seoul"])
    refund_ok = _any(hotels_text, [
        "refundable", "non-refundable", "refund", "cancellation", "cancel",
    ])

    # Cancellation advice must be durable in hotels.md.
    advice_ok = _any(hotels_text, ["non-refundable", "risk", "refund policy", "cancellation policy"])

    ok = used_search and city_ok and hotels_ok and refund_ok and advice_ok
    logger.info(
        f"s3_gate: search={used_search} city={city_ok}(tokyo={has_tokyo},seoul={has_seoul}) "
        f"hotels_md={hotels_ok} refund={refund_ok} advice={advice_ok} → {'PASS' if ok else 'FAIL'}"
    )
    return ok


CHECKS = [("s3_gate", s3_gate, 1.5)]
