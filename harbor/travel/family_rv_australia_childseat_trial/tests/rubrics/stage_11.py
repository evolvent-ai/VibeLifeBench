from __future__ import annotations
from ._helpers import *

def s11_detect_parking_mismatch(env) -> bool:
    return _used_hotel_lookup(env, 11) and _cbr_parking_limit_backend_ready(env) and _check_text(env, 11, [['2.1', '2.1m'], ['2.85', 'motorhome', 'rv'], ['does not fit', 'insufficient', 'mismatch']])

def s11_recover_cbr_parking(env) -> bool:
    return _used_hotel_lookup(env, 11) and _used_maps_parking_search(env, 11) and _parking_recovery_backend_ready(env) and _used_hotel_recovery_action(env, 11) and _any_workspace_file_has(env, [FILE_RISK_LOG, FILE_ORDER_LOG], [['2.1', 'underground'], ['2.85', 'motorhome', 'rv'], ['off-site', 'external', 'alternative', 'rebook'], ['clearance', 'parking']])

def s11_record_weather_risk(env) -> bool:
    return _used_weather_alerts(env, 11) and _tool_args_canberra_weather(env, 11) and _act_wind_alert_backend_ready(env) and _workspace_file_has(env, FILE_RISK_LOG, [['act', 'canberra', 'Canberra'], ['severe wind', 'wind'], ['caution', 'risk'], ['driving', 'route', 'parking']])
CHECKS = [('s11_detect_parking_mismatch', s11_detect_parking_mismatch, 1.75), ('s11_recover_cbr_parking', s11_recover_cbr_parking, 2.0), ('s11_record_weather_risk', s11_record_weather_risk, 2.0)]
