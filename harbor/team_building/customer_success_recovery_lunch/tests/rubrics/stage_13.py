from __future__ import annotations
from ._helpers import *

def s13_license_reverify(env) -> bool:
    return (
        used(env, 13, 'email')
        and used(env, 13, 'email', 'save_draft')
        and any_write(env, 13)
        and state_has(env, 13, [['facilitator'], ['credentials'], ['script'], ['missing'], ['finalizing', 'hold', 'pending']])
    )

CHECKS = [
    ('s13_license_reverify', s13_license_reverify, 1.5),
]
