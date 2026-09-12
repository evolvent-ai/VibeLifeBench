from __future__ import annotations

from ._helpers import _tool_call_count, _workspace_file_text, text_has


def s12_rail_calendar_buffer(env) -> bool:
    rail_reads = _tool_call_count(env, ["rail_booking__search_trains"], 12)
    calendar_writes = _tool_call_count(env, ["calendar__create_event", "calendar__update_event"], 12)
    durable = text_has(
        _workspace_file_text(env, "trip_plan.md") + _workspace_file_text(env, "risk_register.md"),
        [["delay", "maintenance", "service delay", "track maintenance"], ["buffer", "transfer", "backup", "time buffer", "connection", "alternative"]],
    )
    return bool(rail_reads >= 1 and calendar_writes >= 1 and durable)


CHECKS = [
    ("s12_rail_calendar_buffer", s12_rail_calendar_buffer, 2.0),
]
