from __future__ import annotations
from ._helpers import *

def s4_vendor_credentials_draft(env) -> bool:
    return (
        used(env, 4, 'email')
        and used(env, 4, 'email', 'save_draft')
        and any_write(env, 4)
        and state_has(env, 4, [['facilitator'], ['credentials'], ['safety'], ['refund', 'change'], ['non-refundable', 'confirmation']])
    )

CHECKS = [
    ('s4_vendor_credentials_draft', s4_vendor_credentials_draft, 1.5),
]
