from __future__ import annotations
from ._helpers import *

def s10_hotel_mutation_rechecked(env) -> bool:
    return trace_has(env, 10, S_HOTEL, "get_room_availability", [[TARGET_HOTEL_ID], ["2026-09"]]) and hotel_stage10_state(env) and evidence_recorded(env, [[TARGET_HOTEL_ID, "Florence"], ["inventory"], ["1", "one"], ["2026-09-07", "refundable"]])

def s10_refundable_florence_hotel_terminal(env) -> bool:
    return has_refundable_hotel(env, "Florence", TARGET_HOTEL_ID) and no_prepaid_hotel(env)

CHECKS = [
    ("s10_hotel_mutation_rechecked", s10_hotel_mutation_rechecked, 1.5),
    ("s10_refundable_florence_hotel_terminal", s10_refundable_florence_hotel_terminal, 2.0),
]
