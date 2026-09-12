from __future__ import annotations
from ._helpers import *

def s16_flight_fee_repriced(env) -> bool:
    return trace_has(env, 16, S_EMAIL, "search_emails", [["change fee", "earlier arrival"]]) and trace_has(env, 16, S_EMAIL, "read_email") and trace_has(env, 16, S_FLIGHT, "get_flight_offer", [[FEE_OFFER_ID]]) and trace_has(env, 16, S_FLIGHT, "price_offer", [[FEE_OFFER_ID]]) and change_fee_live_is(env)

def s16_fee_change_recorded(env) -> bool:
    return s16_flight_fee_repriced(env) and backend_live_change_fee_state(env) and evidence_recorded(env, [["AZ611"], ["change fee", "change cost"], ["380"]])

CHECKS = [
    ("s16_flight_fee_repriced", s16_flight_fee_repriced, 1.75),
    ("s16_fee_change_recorded", s16_fee_change_recorded, 1.0),
]
