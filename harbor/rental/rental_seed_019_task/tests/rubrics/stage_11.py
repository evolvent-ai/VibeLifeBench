from __future__ import annotations
from ._helpers import *

def s11_archived_repair_found(env) -> bool:
    return stage_read_email_ids(env, 11, ('2',)) and tool_stage(env, 11, 'email', 'read_email', ['msg_repair_20251006'])

def s11_repair_link_restored(env) -> bool:
    return tool_stage(env, 11, 'notion', None, ['msg_repair_20251006']) and tool_stage(env, 11, 'notion', None, ['archive'])

CHECKS = [
    ('s11_archived_repair_found', s11_archived_repair_found, 1.75),
    ('s11_repair_link_restored', s11_repair_link_restored, 1.5),
]
