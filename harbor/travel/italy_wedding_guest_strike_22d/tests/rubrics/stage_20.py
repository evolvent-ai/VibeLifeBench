from __future__ import annotations
from ._helpers import *

def s20_return_status_checked(env) -> bool:
    return (
        trace_has(env, 20, S_FLIGHT, "get_flight_status", [["UA971"], ["2026-09-15"]])
        and trace_has(env, 20, S_HOTEL, "list_reservations", [[USER_ID]])
        and trace_has(env, 20, S_WEATHER, "get_alerts", [["Rome"]])
        and flight_status_current(env, "UA971", "2026-09-15", "2026-09-13T08:45:00Z", "E7")
        and flight_route_booked(env, "FCO", "EWR", "2026-09-15", refundable=True)
        and has_refundable_hotel(env, "Rome", "hotel_roma_aventino_019")
    )

def s20_return_recorded(env) -> bool:
    return s20_return_status_checked(env) and evidence_recorded(env, [["return"], ["UA971", "Rome"], ["checkout"], [S_WEATHER, "weather"], ["status"]])

CHECKS = [
    ("s20_return_status_checked", s20_return_status_checked, 1.25),
    ("s20_return_recorded", s20_return_recorded, 1.0),
]
