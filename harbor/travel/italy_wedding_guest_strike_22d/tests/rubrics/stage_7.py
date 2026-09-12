from __future__ import annotations
from ._helpers import *

def s7_scheduled_refresh_broad(env) -> bool:
    return (
        trace_has(env, 7, S_FLIGHT, "list_bookings", [[USER_EMAIL]])
        and trace_has(env, 7, S_HOTEL, "list_reservations", [[USER_ID]])
        and trace_has(env, 7, S_RAIL, "get_train_status", [["FR9403"]])
        and trace_has(env, 7, S_WEATHER, "get_alerts", [["Florence"]])
        and trace_has(env, 7, S_REVIEW, "list_reservations", [[USER_ID]])
        and trace_has(env, 7, S_CARD, "list_cards", [[USER_ID]])
        and trace_any(env, 7, [(S_CALENDAR, "search_events", [["wedding"]]), (S_CALENDAR, "list_events", [["2026-09"]])])
        and trace_has(env, 7, S_NOTION, "API-post-search", [["Italy", "Wedding"]])
    )

def s7_heartbeat_updated(env) -> bool:
    return s7_scheduled_refresh_broad(env) and backend_restaurant_absence_safe(env) and file_has(env, "HEARTBEAT.md", [["open", "pending", "unresolved"], ["flight"], ["hotel"], ["rail"], ["restaurant"]])

CHECKS = [
    ("s7_scheduled_refresh_broad", s7_scheduled_refresh_broad, 1.25),
    ("s7_heartbeat_updated", s7_heartbeat_updated, 0.1),
]
