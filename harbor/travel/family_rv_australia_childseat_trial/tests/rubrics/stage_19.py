from __future__ import annotations
from ._helpers import *

def s19_update_melbourne_route(env) -> bool:
    return _used_maps_route(env, 19) and _calendar_write_in_stage(env, 19) and _check_text(env, 19, [['albury', 'melbourne', 'Melbourne'], ['driving route', 'route']])

def s19_avoid_night_and_peak(env) -> bool:
    return _check_text(env, 19, [['dark', 'no night'], ['traffic', 'peak'], ['Melbourne', 'melbourne']])
CHECKS = [('s19_update_melbourne_route', s19_update_melbourne_route, 2.0), ('s19_avoid_night_and_peak', s19_avoid_night_and_peak, 2.0)]
