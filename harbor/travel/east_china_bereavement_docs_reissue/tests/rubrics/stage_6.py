from __future__ import annotations
from ._helpers import check_s6_update_funeral_calendar, check_s6_avoid_extra_uncle_ping

def s6_update_funeral_calendar(env) -> bool:
    return check_s6_update_funeral_calendar(env)

def s6_avoid_extra_uncle_ping(env) -> bool:
    return check_s6_avoid_extra_uncle_ping(env)

CHECKS = [
    ("s6_update_funeral_calendar", s6_update_funeral_calendar, 1),
    ("s6_avoid_extra_uncle_ping", s6_avoid_extra_uncle_ping, 1),
]
