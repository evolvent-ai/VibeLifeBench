from __future__ import annotations
from ._helpers import check_s16_elder_ticket_card

def s16_elder_ticket_card(env) -> bool:
    return check_s16_elder_ticket_card(env)

CHECKS = [
    ("s16_elder_ticket_card", s16_elder_ticket_card, 2),
]
