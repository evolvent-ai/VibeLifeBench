from __future__ import annotations
from ._helpers import *

def s18_final_pre_wedding_refresh(env) -> bool:
    return (
        trace_has(env, 18, S_RAIL, "get_train_status", [["FR9505"], ["2026-09-11"]])
        and trace_has(env, 18, S_FLIGHT, "list_bookings", [[USER_EMAIL]])
        and trace_has(env, 18, S_HOTEL, "list_reservations", [[USER_ID]])
        and trace_has(env, 18, S_REVIEW, "list_reservations", [[USER_ID]])
        and trace_has(env, 18, S_CALENDAR, "search_events", [["rehearsal", "wedding"]])
        and trace_has(env, 18, S_WEATHER, "get_alerts", [["Florence"]])
        and trace_has(env, 18, S_MAPS, "get_traffic_estimate", [["Florence", "pl_florence_smn"], ["Wedding", "Villa", "pl_villa_arno"]])
        and trace_has(env, 18, S_CARD, "list_cards", [[USER_ID]])
        and trace_has(env, 18, S_NOTION, "API-post-search", [["Italy", "Wedding"]])
    )

def s18_rehearsal_and_hotel_restaurant_aligned(env) -> bool:
    return s18_final_pre_wedding_refresh(env) and restaurant_reserved_safe(env) and has_refundable_hotel(env, "Florence", TARGET_HOTEL_ID) and backend_calendar_weather_state_complete(env) and evidence_recorded(env, [["rehearsal"], ["hotel"], ["restaurant"], ["wedding"], ["weather", "rain"], ["buffer", "traffic", "route"]])

CHECKS = [("s18_rehearsal_and_hotel_restaurant_aligned", s18_rehearsal_and_hotel_restaurant_aligned, 1.75)]
