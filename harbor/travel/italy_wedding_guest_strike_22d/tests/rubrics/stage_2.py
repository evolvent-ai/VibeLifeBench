from __future__ import annotations

from ._helpers import *

def s2_calendar_budget_checked(env) -> bool:
    return (trace_any(env, 2, [(S_CALENDAR, "search_events", [["wedding"]]), (S_CALENDAR, "list_events", [["2026-09-12"]])]) and backend_wedding_calendar_state(env) and budget_recorded(env, [["4800", "4,800"], ["EUR", "euro"]]))

def s2_wedding_calendar_preserved(env) -> bool:
    return (
        trace_any(env, 2, [(S_CALENDAR, "search_events", [["wedding"]]), (S_CALENDAR, "list_events", [["2026-09-12"]])])
        and backend_wedding_calendar_state(env)
        and evidence_recorded(env, [["wedding"], ["15:30", "3:30"], ["calendar", "ceremony"]])
    )

CHECKS = [
    ("s2_calendar_budget_checked", s2_calendar_budget_checked, 1.25),
    ("s2_wedding_calendar_preserved", s2_wedding_calendar_preserved, 0.8),
]
