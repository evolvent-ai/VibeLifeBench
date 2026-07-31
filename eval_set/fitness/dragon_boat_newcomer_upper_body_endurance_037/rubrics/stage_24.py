from __future__ import annotations
from ._helpers import _check

def chk_s24_venue_maintenance_replan_no_booking(env) -> bool:
    return _check('chk_s24_venue_maintenance_replan_no_booking', env)

def chk_s24_maintenance_read_no_booking_light(env) -> bool:
    return _check('chk_s24_maintenance_read_no_booking_light', env)

def chk_s24_venue_calendar_action_light(env) -> bool:
    return _check('chk_s24_venue_calendar_action_light', env)

CHECKS = [
    ('chk_s24_venue_maintenance_replan_no_booking', chk_s24_venue_maintenance_replan_no_booking, 1.75),
    ('chk_s24_maintenance_read_no_booking_light', chk_s24_maintenance_read_no_booking_light, 1.0),
    ('chk_s24_venue_calendar_action_light', chk_s24_venue_calendar_action_light, 1.0)
]
