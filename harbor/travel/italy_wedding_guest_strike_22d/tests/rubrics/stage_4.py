from __future__ import annotations
from ._helpers import *

def s4_hotels_maps_checked(env) -> bool:
    return (
        trace_has(env, 4, S_HOTEL, "search_hotels", [["Florence"], ["2026-09"]])
        and trace_has(env, 4, S_HOTEL, "get_room_availability", [[TARGET_HOTEL_ID], ["2026-09"]])
        and trace_has(env, 4, S_MAPS, "directions", [["Santa Maria Novella", "pl_florence_smn"], ["Wedding", "Villa", "pl_villa_arno"]])
        and trace_has(env, 4, S_MAPS, "distance_matrix", [["Florence", "pl_florence_smn"]])
        and trace_any(env, 4, [(S_FLIGHT, "get_flight_offer", [[FEE_OFFER_ID]]), (S_FLIGHT, "price_offer", [[FEE_OFFER_ID]])])
        and change_fee_live_is(env, fee=260)
    )

def s4_refund_window_recorded(env) -> bool:
    return s4_hotels_maps_checked(env) and evidence_recorded(env, [["Florence"], ["hotel"], ["refund", "refundable", "cancellation"], ["AZ611", "260"]])

CHECKS = [("s4_refund_window_recorded", s4_refund_window_recorded, 1.0)]
