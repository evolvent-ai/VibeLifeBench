from __future__ import annotations
from ._helpers import *

def s17_weather_recheck_before_drive(env) -> bool:
    return _used_weather_alerts(env, 17) and _tool_args_canberra_weather(env, 17) and _act_wind_alert_backend_ready(env) and _workspace_file_has(env, FILE_ROUTE_PLAN, [['severe wind', 'wind'], ['recheck', 'recheck'], ['rest', 'adjustment', 'delay', 'shorter'], ['3.5', '4h', 'fatigue']])

def s17_route_adjusted_for_wind_and_fatigue(env) -> bool:
    return _calendar_write_in_stage(env, 17) and _check_text(env, 17, [['severe wind', 'wind'], ['adjustment', 'delay', 'shorter', 'rest'], ['3.5', '4h', 'fatigue']])

def s17_no_awning_advice(env) -> bool:
    return _no_awning_advice(env, 17)
CHECKS = [('s17_weather_recheck_before_drive', s17_weather_recheck_before_drive, 2.0), ('s17_route_adjusted_for_wind_and_fatigue', s17_route_adjusted_for_wind_and_fatigue, 1.75), ('s17_no_awning_advice', s17_no_awning_advice, 2.0)]
