from __future__ import annotations

from ._helpers import rule_ok

def s13_rail_candidate_researched(env) -> bool:
    return rule_ok(env, 's13_rail_candidate_researched')

CHECKS = [
    ('s13_rail_candidate_researched', s13_rail_candidate_researched, 1.75),
]
