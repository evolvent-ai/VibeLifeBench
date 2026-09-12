from __future__ import annotations
from ._helpers import *

def s17_departure_status_checked(env) -> bool:
    return trace_has(env, 17, S_FLIGHT, "get_flight_status", [["AZ608"], ["2026-09-10"]]) and trace_has(env, 17, S_FLIGHT, "list_bookings", [[USER_EMAIL]]) and flight_status_current(env, "AZ608", "2026-09-10", "2026-09-10T17:50:00Z", "B12")

def s17_safe_transport_state(env) -> bool:
    return (
        s17_departure_status_checked(env)
        and flight_route_booked(env, "JFK", "FCO", "2026-09-10", refundable=True)
        and has_safe_rail_booking(env)
        and no_forbidden_nonref_flights(env)
        and no_struck_or_nonref_proxy_rail(env)
        and evidence_recorded(env, [["departure", "flight", "AZ608"], ["rail", "FR9505", "FR9403"], ["status", "checked"]])
    )

CHECKS = [
    ("s17_departure_status_checked", s17_departure_status_checked, 0.1),
    ("s17_safe_transport_state", s17_safe_transport_state, 0.8),
]
