from __future__ import annotations
from ._helpers import *

def s16_newcomer_mixed_groups(env) -> bool:
    recorded = stage_persisted(env, 16, [["opt-out"], ["no-photography"], ["staggered"], ["private", "minimum"]])
    return recorded

CHECKS = [
    ('s16_newcomer_mixed_groups', s16_newcomer_mixed_groups, 1.25),
]
