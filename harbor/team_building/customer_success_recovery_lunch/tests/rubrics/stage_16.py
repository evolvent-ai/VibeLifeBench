from __future__ import annotations
from ._helpers import *

def s16_approver_safety_requirements(env) -> bool:
    return (
        used(env, 16, 'email')
        and (used(env, 16, 'email', 'save_draft') or used(env, 16, 'notification_hub') or used(env, 16, 'notion'))
        and any_write(env, 16)
        and state_has(env, 16, [['opt out'], ['halal', 'lactose-free', 'lactose', 'dairy'], ['quiet'], ['privacy'], ['notice', 'window']])
    )

CHECKS = [
    ('s16_approver_safety_requirements', s16_approver_safety_requirements, 1.25),
]
