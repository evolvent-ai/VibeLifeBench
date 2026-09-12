"""Stage 10: notification — EVUS reminder."""
from __future__ import annotations
from loguru import logger
from ._helpers import _tool_called_in_stage, _stage_text, _any

# Real visa tools that read an EVUS renewal application. The former
# get_evus_status tool was not exposed by the visa service.
_EVUS_READ_TOOLS = ["list_visa_applications", "get_visa_application", "check_entry_requirements"]


def s10_checked_evus(env) -> bool:
    """Stage 10 checked the EVUS renewal via a real visa tool AND the response shows the agent
    understood EVUS needs renewal (parts: tool used in stage + narration evidence)."""
    tool_ok = _tool_called_in_stage(env, 10, _EVUS_READ_TOOLS)
    text = _stage_text(env, 10).lower()
    understood = _any(text, ["evus", "expired", "expire", "invalid", "renewal", "2026-03-25"])
    ok = tool_ok and understood
    logger.info(f"s10_checked_evus: tool_ok={tool_ok} understood={understood} -> {ok}")
    return ok


CHECKS = [
    ("s10_checked_evus", s10_checked_evus, 1.0),
]
