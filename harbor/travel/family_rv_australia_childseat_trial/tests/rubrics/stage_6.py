from __future__ import annotations
from ._helpers import *

def s6_lock_refundable_rv(env) -> bool:
    return _used_car_create_booking(env, 6) and _has_car_booking(env, [['southerncross', '4b'], ['held', 'confirmed'], ['free_cancel', 'refundable', 'cancellable']])

def s6_childseat_addon_confirmed(env) -> bool:
    return _has_car_booking(env, [['child', 'child restraint'], ['approved', 'as/nzs', 'compliant']])

def s6_full_rv_insurance_selected(env) -> bool:
    return _has_car_booking(env, [['full', 'plus', 'insurance', 'coverage'], ['motorhome', 'rv', 'rental']])

def s6_one_way_return_valid(env) -> bool:
    return _used_car_create_booking(env, 6) and _has_car_booking(env, [['sydney', 'Sydney'], ['melbourne', 'Melbourne'], ['one_way', 'one-way']]) and _workspace_file_has(env, FILE_ORDER_LOG, [['southerncross', 'motorhome', 'rv'], ['sydney', 'Sydney'], ['melbourne', 'Melbourne'], ['one-way', 'one-way'], ['cancellable', 'refundable']])

def s6_book_cbr_parking_hotel(env) -> bool:
    return _used_hotel_create(env, 6) and _booked_canberra_rv_hotel_backend_ready(env) and _workspace_file_has(env, FILE_ORDER_LOG, [['canberra', 'Canberra'], ['rv', 'parking', 'clearance'], ['3.2', 'outdoor', 'open-air'], ['refundable', 'cancellable']])
CHECKS = [('s6_lock_refundable_rv', s6_lock_refundable_rv, 2.0), ('s6_childseat_addon_confirmed', s6_childseat_addon_confirmed, 2.0), ('s6_full_rv_insurance_selected', s6_full_rv_insurance_selected, 2.0), ('s6_one_way_return_valid', s6_one_way_return_valid, 2.0), ('s6_book_cbr_parking_hotel', s6_book_cbr_parking_hotel, 2.0)]
