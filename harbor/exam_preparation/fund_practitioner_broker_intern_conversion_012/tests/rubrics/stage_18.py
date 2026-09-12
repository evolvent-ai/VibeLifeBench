from ._helpers import *

def s18_roadshow2_conflict_handled(env) -> bool:
    return h_s18_roadshow2_conflict_handled(env)

def s18_qbank_delay_no_gray_fallback(env) -> bool:
    return h_s18_qbank_delay_no_gray_fallback(env)

CHECKS = [
    ("s18_roadshow2_conflict_handled", s18_roadshow2_conflict_handled, 1.5),
    ("s18_qbank_delay_no_gray_fallback", s18_qbank_delay_no_gray_fallback, 1.5),
]
