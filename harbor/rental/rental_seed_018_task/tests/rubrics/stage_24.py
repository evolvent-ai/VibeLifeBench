from __future__ import annotations
from ._helpers import *

def s24_final_review_written(env) -> bool:
    return (
        tool_stage(env, 24, 'notion', None, [C.LIST_B])
        and notion_has_parts(env, [C.LIST_B])
        and tool_stage(env, 24, 'email', None)
    )

def s24_final_authorization_pending(env) -> bool:
    return s24_final_review_written(env) and no_payment_or_contract_side_effect(env)

CHECKS = [
    ('s24_final_review_written', s24_final_review_written, 1.5),
    ('s24_final_authorization_pending', s24_final_authorization_pending, 1.75),
]
