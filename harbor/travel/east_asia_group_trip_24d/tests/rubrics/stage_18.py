"""Stage 18: a real JST medication reminder plus Zhao Min's zero Seoul actual allocation."""
from __future__ import annotations

from loguru import logger

from ._helpers import _calendar_events, _tool_calls, _tool_name_matches, _workspace_file_text


def s18_gate(env) -> bool:
    create_calls = [c for c in _tool_calls(env, 18) if _tool_name_matches(str(c.get("name") or ""), "calendar", "create_event")]
    exact_call = any(
        isinstance(c.get("arguments"), dict)
        and "+09:00" in str(c["arguments"].get("start") or "")
        and isinstance(c["arguments"].get("reminders"), list) and bool(c["arguments"].get("reminders"))
        and any(x in str(c["arguments"].get("summary") or "").casefold() for x in ("medication", "medicine"))
        for c in create_calls
    )
    backend = [e for e in _calendar_events(env) if any(x in str(e.get("summary") or "").casefold() for x in ("medication", "medicine")) and "+09:00" in str(e.get("start") or e.get("start_time") or "")]
    backend_ok = any(isinstance(e.get("reminders"), list) and bool(e.get("reminders")) for e in backend)
    budget = _workspace_file_text(env, "/workspace/budget.md").casefold()
    actual_ok = (
        "actual" in budget
        and "usr_zhao_min" in budget
        and any(x in budget for x in ("seoul_minor=0", "seoul_minor = 0"))
    )
    result = exact_call and backend_ok and actual_ok
    logger.info("s18_gate: call={} backend={} actual={} -> {}", exact_call, backend_ok, actual_ok, "PASS" if result else "FAIL")
    return result


CHECKS = [("s18_gate", s18_gate, 1.5)]
