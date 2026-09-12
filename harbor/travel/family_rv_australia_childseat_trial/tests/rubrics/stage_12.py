from __future__ import annotations
from ._helpers import *

def s12_detect_insurance_addendum(env) -> bool:
    return _used_car_insurance_or_booking(env, 12) and _insurance_wind_addendum_backend_ready(env) and _workspace_file_has(env, FILE_RISK_LOG, [['2026-09-17-wind', 'addendum', 'policy'], ['awning', 'secured'], ['not covered', 'excluded', 'restriction'], ['severe wind', 'wind']])

def s12_update_user_safety_guidance(env) -> bool:
    return _check_text(env, 12, [['severe wind', 'wind'], ['secured', 'awning'], ['do not', 'avoid', 'latched'], ['user', 'reminder']])

def s12_adjust_route_or_calendar_for_wind(env) -> bool:
    return _calendar_write_in_stage(env, 12) and _check_text(env, 12, [['severe wind', 'wind'], ['journey', 'route'], ['reduced', 'adjustment', 'delay', 'rest']])
CHECKS = [('s12_detect_insurance_addendum', s12_detect_insurance_addendum, 1.75), ('s12_update_user_safety_guidance', s12_update_user_safety_guidance, 2.0), ('s12_adjust_route_or_calendar_for_wind', s12_adjust_route_or_calendar_for_wind, 1.75)]
