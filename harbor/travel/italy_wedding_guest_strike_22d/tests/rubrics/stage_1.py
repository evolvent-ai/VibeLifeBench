from __future__ import annotations
from ._helpers import *

def s1_email_and_hotel_block_checked(env) -> bool:
    return (
        trace_has(env, 1, S_EMAIL, "search_emails", [["wedding"]])
        and trace_has(env, 1, S_EMAIL, "read_email")
        and trace_has(env, 1, S_HOTEL, "search_hotels", [["Florence"], ["2026-09"]])
        and trace_has(env, 1, S_HOTEL, "get_room_availability", [[TARGET_HOTEL_ID], ["2026-09"]])
    )

def s1_stale_email_risk_recorded(env) -> bool:
    return (
        s1_email_and_hotel_block_checked(env)
        and wedding_email_present(env)
        and hotel_inventory_available(env)
        and evidence_recorded(env, [["hotel", S_EMAIL], ["live", "verify", "current"], ["Florence"]])
    )

CHECKS = [
    ("s1_email_and_hotel_block_checked", s1_email_and_hotel_block_checked, 1.25),
    ("s1_stale_email_risk_recorded", s1_stale_email_risk_recorded, 1.0),
]
