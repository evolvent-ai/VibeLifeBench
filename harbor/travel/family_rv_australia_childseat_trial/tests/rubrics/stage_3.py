from __future__ import annotations
from ._helpers import *

def s3_compare_flight_and_rv_options(env) -> bool:
    return _used_flight_search(env, 3) and _used_car_offer_search(env, 3) and _check_text(env, 3, [['pvg', 'Shanghai'], ['syd', 'Sydney'], ['southerncross', 'tasman', 'pacific'], ['compare', 'candidate']])

def s3_filter_noncompliant_rv(env) -> bool:
    return _used_car_offer_search(env, 3) and _no_nonrefundable_rv_booking(env) and _check_text(env, 3, [['tasman', 'nonrefundable', 'non-refundable'], ['child restraint', 'child'], ['exclude', 'reject', 'not selected']])

def s3_subscribe_weather_alerts(env) -> bool:
    return _used_weather_subscribe(env, 3) and _weather_subscription_trace_complete(env) and _any_workspace_file_has(env, [FILE_ROUTE_PLAN, FILE_RISK_LOG], [['forecast', 'weather'], ['alert', 'warning', 'subscribe'], ['nsw', 'sydney', 'act', 'canberra'], ['vic', 'melbourne']])

def s3_route_fatigue_first_pass(env) -> bool:
    return _used_maps_route(env, 3) and _check_text(env, 3, [['3.5', 'limits', 'duration'], ['night', 'no night'], ['recovery', 'rest']])
CHECKS = [('s3_compare_flight_and_rv_options', s3_compare_flight_and_rv_options, 2.0), ('s3_filter_noncompliant_rv', s3_filter_noncompliant_rv, 1.75), ('s3_subscribe_weather_alerts', s3_subscribe_weather_alerts, 1.5), ('s3_route_fatigue_first_pass', s3_route_fatigue_first_pass, 2.0)]
