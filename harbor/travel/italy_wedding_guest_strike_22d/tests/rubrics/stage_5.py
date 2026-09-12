from __future__ import annotations

from ._helpers import *

def s5_rail_and_calendar_checked(env) -> bool:
    return (trace_any(env, 5, [(S_RAIL, "search_trains", [["Milan"], ["Florence"], ["2026-09-11"]])]) and trace_any(env, 5, [(S_CALENDAR, "search_events", [["wedding"]])]))

def s5_route_buffer_recorded(env) -> bool:
    return (trace_any(env, 5, [(S_RAIL, "search_trains", [["Milan"], ["Florence"], ["2026-09-11"]])]) and backend_wedding_calendar_state(env) and evidence_recorded(env, [["Milan", "Florence"], ["rail"], ["buffer", "ceremony", "15:30"]]))

CHECKS = [
    ("s5_rail_and_calendar_checked", s5_rail_and_calendar_checked, 1.25),
    ("s5_route_buffer_recorded", s5_route_buffer_recorded, 1.0),
]
