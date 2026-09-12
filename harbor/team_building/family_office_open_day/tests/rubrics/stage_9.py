from __future__ import annotations
from ._helpers import *

def s9_roster_minimized_counts(env) -> bool:
    recorded = stage_persisted(env, 9, [["60"], ["36"], ["22"], ["attendance"], ["minimum"]])
    return recorded

CHECKS = [
    ('s9_roster_minimized_counts', s9_roster_minimized_counts, 1.5),
]
