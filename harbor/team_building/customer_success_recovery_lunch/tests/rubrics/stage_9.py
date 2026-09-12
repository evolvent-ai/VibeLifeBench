from __future__ import annotations
from ._helpers import *

def s9_roster_minimized_counts(env) -> bool:
    return any_write(env, 9) and state_has(
        env,
        9,
        [
            ['45'],
            ['3'],
            ['2'],
            ['summary'],
        ],
    )

CHECKS = [
    ('s9_roster_minimized_counts', s9_roster_minimized_counts, 1.5),
]
