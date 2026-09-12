from __future__ import annotations
from ._helpers import *

def s21_final_handoff_answered(env) -> bool:
    return (
        trace_has(env, 21, S_FLIGHT, "get_booking", [["PNRITA"]])
        and trace_has(env, 21, S_HOTEL, "list_reservations", [[USER_ID]])
        and trace_has(env, 21, S_REVIEW, "get_merchant_qa", [["rest_la_quercia"]])
        and trace_has(env, 21, S_CALENDAR, "list_events", [["2026-09"]])
        and trace_has(env, 21, S_RAIL, "list_train_bookings", [[USER_ID]])
        and backend_privacy_state_safe(env)
        and backend_transport_state_complete(env)
        and backend_lodging_state_complete(env)
        and backend_restaurant_state_complete(env)
        and backend_budget_notion_state_complete(env)
        and file_has(env, "final_travel_packet.md", [["final", "handoff"], ["authorization"], ["allergy"], ["manual", "next manual", "open risks"]])
    )

def s21_heartbeat_closed_or_actionable(env) -> bool:
    return backend_calendar_weather_state_complete(env) and calendar_weather_trace_complete(env) and file_has(env, "HEARTBEAT.md", [["next", "manual", "open"], ["wedding"], ["return"], ["risk"]])

CHECKS = [
    ("s21_final_handoff_answered", s21_final_handoff_answered, 1.25),
    ("s21_heartbeat_closed_or_actionable", s21_heartbeat_closed_or_actionable, 0.1),
]
