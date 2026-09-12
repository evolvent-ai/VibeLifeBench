from __future__ import annotations
from ._helpers import *

def s14_detect_flight_schedule_change(env) -> bool:
    return _used_flight_status(env, 14) and _tool_args_outbound_flight(env, 14) and _outbound_schedule_change_backend_ready(env) and _any_workspace_file_has(env, [FILE_ORDER_LOG, FILE_ROUTE_PLAN], [['sc888'], ['19:45', 'earlier', '45'], ['pvg', 'Shanghai'], ['syd', 'Sydney']])

def s14_update_calendar_and_user(env) -> bool:
    return _calendar_write_in_stage(env, 14) and _check_text(env, 14, [['19:45', 'earlier', '45'], ['notify', 'reminder', 'departure']])

def s14_late_arrival_email(env) -> bool:
    return _email_action_in_stage(env, 14) and _has_email(env, [['late', 'late arrival'], ['sydney', 'Sydney', 'hotel', 'accommodation']])
CHECKS = [('s14_detect_flight_schedule_change', s14_detect_flight_schedule_change, 1.75), ('s14_update_calendar_and_user', s14_update_calendar_and_user, 2.0), ('s14_late_arrival_email', s14_late_arrival_email, 1.5)]
