from __future__ import annotations
from ._helpers import evaluate

def chk_s07_calendar_mutation_discovered(env) -> bool:
    return evaluate('chk_s07_calendar_mutation_discovered', env)

def chk_s07_conflict_calendar_adjusted(env) -> bool:
    return evaluate('chk_s07_conflict_calendar_adjusted', env)

CHECKS = [
    ('chk_s07_calendar_mutation_discovered', chk_s07_calendar_mutation_discovered, 1.75),
    ('chk_s07_conflict_calendar_adjusted', chk_s07_conflict_calendar_adjusted, 1.5),
]
