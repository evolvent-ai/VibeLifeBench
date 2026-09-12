from __future__ import annotations
from ._helpers import *

def s1_update_goal_constraints(env) -> bool:
    return (
        used(env, 1, 'email')
        and any_write(env, 1)
        and state_has(env, 1, [['recovery'], ['cross-team'], ['voluntary', 'low-pressure', 'stress-relief'], ['forced', 'public'], ['psychological']])
    )

CHECKS = [
    ('s1_update_goal_constraints', s1_update_goal_constraints, 1.5),
]
