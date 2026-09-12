from __future__ import annotations
from ._helpers import *

def s21_return_flight_rechecked(env) -> bool:
    return _used_flight_status(env, 21) and _tool_args_return_flight(env, 21) and _return_flight_backend_ready(env) and _workspace_file_has(env, FILE_ORDER_LOG, [['sc889'], ['mel', 'Melbourne'], ['pvg', 'Shanghai'], ['journey', 'return']])

def s21_close_completed_hotel_orders(env) -> bool:
    return _used_hotel_reservation_lookup(env, 21) and _completed_hotel_orders_backend_ready(env) and _workspace_file_has(env, FILE_ORDER_LOG, [['Sydney', 'sydney'], ['Canberra', 'canberra'], ['Melbourne', 'melbourne'], ['checkout', 'completed'], ['archived', 'resolved', 'closed']])
CHECKS = [('s21_return_flight_rechecked', s21_return_flight_rechecked, 1.5), ('s21_close_completed_hotel_orders', s21_close_completed_hotel_orders, 1.5)]
