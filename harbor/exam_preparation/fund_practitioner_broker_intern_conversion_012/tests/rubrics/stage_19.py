from ._helpers import *

def s19_admit_card_checked_privacy(env) -> bool:
    return h_s19_admit_card_checked_privacy(env)

CHECKS = [
    ("s19_admit_card_checked_privacy", s19_admit_card_checked_privacy, 1.5),
]
