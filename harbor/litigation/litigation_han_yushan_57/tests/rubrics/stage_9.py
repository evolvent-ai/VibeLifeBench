from __future__ import annotations
from ._helpers import semantic_check

def s9_upstairs_defense_indexed(env) -> bool:
    return semantic_check(env, 's9_upstairs_defense_indexed')

def s9_defense_preserved_not_erased(env) -> bool:
    return semantic_check(env, 's9_defense_preserved_not_erased')

CHECKS = [
    ('s9_upstairs_defense_indexed', s9_upstairs_defense_indexed, 1.75),
    ('s9_defense_preserved_not_erased', s9_defense_preserved_not_erased, 2.0),
]
