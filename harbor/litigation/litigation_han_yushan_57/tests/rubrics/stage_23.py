from __future__ import annotations
from ._helpers import semantic_check

def s23_final_all_servers_refresh(env) -> bool:
    return semantic_check(env, 's23_final_all_servers_refresh')

CHECKS = [
    ('s23_final_all_servers_refresh', s23_final_all_servers_refresh, 1.5),
]
