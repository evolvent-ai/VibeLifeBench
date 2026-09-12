from __future__ import annotations
from ._helpers import check_s5_restore_elder_lodging, check_s5_ledger_hotel_delta

def s5_restore_elder_lodging(env) -> bool:
    return check_s5_restore_elder_lodging(env)

def s5_ledger_hotel_delta(env) -> bool:
    return check_s5_ledger_hotel_delta(env)

CHECKS = [
    ("s5_restore_elder_lodging", s5_restore_elder_lodging, 1.5),
    ("s5_ledger_hotel_delta", s5_ledger_hotel_delta, 1.5),
]
