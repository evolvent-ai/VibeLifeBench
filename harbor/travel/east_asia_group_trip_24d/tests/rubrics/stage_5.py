"""Stage 5 gate: add the fixed Tokyo meeting to the calendar and itinerary."""
from __future__ import annotations

from loguru import logger

from ._helpers import (
    _agent_used_tool,
    _agent_tool_args_text,
    _calendar_events,
    _workspace_file_text,
    _any,
)


def s5_gate(env) -> bool:
    """Call create_event with the June 6 Tokyo timezone anchor and persist it."""
    used_create = _agent_used_tool(env, "calendar", "create_event", stage=5)

    args = _agent_tool_args_text(env, stage=5)
    has_date = _any(args, ["06-06", "06/06", "2026-06-06", "6-6"])
    has_tz = _any(args, ["asia/tokyo", "tokyo", "+09", "jst", "japan"])

    # The calendar backend must contain a dated meeting event.
    cal_ok = False
    for ev in _calendar_events(env):
        start = str(ev.get("start") or ev.get("start_time") or "").lower()
        summary = str(ev.get("summary") or ev.get("title") or "").lower()
        if ("06-06" in start or "06/06" in start) and _any(summary, ["meeting", "conference", "anchor"]):
            cal_ok = True
            break

    # itinerary.md must record the meeting anchor.
    itinerary = _workspace_file_text(env, "/workspace/itinerary.md").lower()
    itin_ok = _any(itinerary, ["meeting", "06-06", "anchor"])

    ok = (used_create and has_date and has_tz) and cal_ok and itin_ok
    logger.info(
        f"s5_gate: create={used_create} date={has_date} tz={has_tz} "
        f"cal={cal_ok} itin={itin_ok} → {'PASS' if ok else 'FAIL'}"
    )
    return ok


CHECKS = [("s5_gate", s5_gate, 1.5)]
