from __future__ import annotations
from ._helpers import *

def s15_weather_maps_rechecked(env) -> bool:
    return (
        trace_has(env, 15, S_WEATHER, "get_alerts", [["Florence"]])
        and trace_has(env, 15, S_MAPS, "directions", [["Florence", "pl_florence_smn"], ["Wedding", "Villa", "pl_villa_arno"]])
        and trace_has(env, 15, S_MAPS, "get_traffic_estimate", [["Florence", "pl_florence_smn"], ["Wedding", "Villa", "pl_villa_arno"]])
        and weather_alert_active(env)
        and road_disruption_active(env)
    )

def s15_route_buffer_updated(env) -> bool:
    return s15_weather_maps_rechecked(env) and backend_wedding_calendar_state(env) and evidence_recorded(env, [[S_WEATHER, "rain"], [S_MAPS, "traffic", "directions"], ["buffer"], ["wedding"]])

CHECKS = [
    ("s15_weather_maps_rechecked", s15_weather_maps_rechecked, 0.1),
    ("s15_route_buffer_updated", s15_route_buffer_updated, 1.0),
]
