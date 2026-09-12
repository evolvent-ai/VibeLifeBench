from __future__ import annotations
from ._helpers import *

def s16_confirm_pickup_childseat_insurance(env) -> bool:
    return (_used_car_booking_lookup(env, 16) or _used_car_return_requirements(env, 16)) and _check_text(env, 16, [['child restraint', 'child'], ['addendum', 'insurance'], ['orientation', 'pickup']])

def s16_reduce_first_drive_due_right_hand(env) -> bool:
    return _calendar_write_in_stage(env, 16) and _check_text(env, 16, [['right-hand-drive', 'right-hand'], ['nervous', 'anxiety'], ['reduced', 'low-speed', 'practice', 'buffer']])

def s16_record_return_requirements(env) -> bool:
    return _used_car_return_requirements(env, 16) and _check_text(env, 16, [['handover', 'return'], ['gauge', 'fuel'], ['cleanliness', 'clean'], ['time', 'deadline']])
CHECKS = [('s16_confirm_pickup_childseat_insurance', s16_confirm_pickup_childseat_insurance, 2.0), ('s16_reduce_first_drive_due_right_hand', s16_reduce_first_drive_due_right_hand, 1.75), ('s16_record_return_requirements', s16_record_return_requirements, 1.5)]
