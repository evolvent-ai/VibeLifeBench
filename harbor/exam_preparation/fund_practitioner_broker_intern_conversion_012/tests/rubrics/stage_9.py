from ._helpers import *

def s9_roadshow_conflict_handled(env) -> bool:
    return h_s9_roadshow_conflict_handled(env)

CHECKS = [
    ("s9_roadshow_conflict_handled", s9_roadshow_conflict_handled, 1.75),
]
