from __future__ import annotations
from ._helpers import *

def s20_authorized_delivery_to_short103(env) -> bool:
    return run_stage_requirement(env, 's20_authorized_delivery_to_short103')

def s20_not_long_term_address(env) -> bool:
    return run_stage_requirement(env, 's20_not_long_term_address')

CHECKS = [
    ('s20_authorized_delivery_to_short103', s20_authorized_delivery_to_short103, 1.75),
    ('s20_not_long_term_address', s20_not_long_term_address, 2.0),
]
