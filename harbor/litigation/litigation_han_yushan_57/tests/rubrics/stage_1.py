from __future__ import annotations
from ._helpers import semantic_check

def s1_all_required_servers_touched(env) -> bool:
    return semantic_check(env, 's1_all_required_servers_touched')

def s1_object_index_created(env) -> bool:
    return semantic_check(env, 's1_object_index_created')

CHECKS = [
    ('s1_all_required_servers_touched', s1_all_required_servers_touched, 1.75),
    ('s1_object_index_created', s1_object_index_created, 1.5),
]
