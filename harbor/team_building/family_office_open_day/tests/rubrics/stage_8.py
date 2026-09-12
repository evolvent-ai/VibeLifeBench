from __future__ import annotations
from ._helpers import *

def s8_scheduled_multi_server_check(env) -> bool:
    checked = sum(1 for server, token in [
        ("review_platform", "search"), ("review_platform", "get"),
        ("maps", "traffic"), ("maps", "directions"),
        ("ecommerce", "search"), ("credit_card", "list"),
    ] if used(env, 8, server, token))
    recorded = stage_persisted(env, 8, [["recheck"], ["venue", "vendor"], ["supplies", "inventory", "traffic"]])
    return checked >= 2 and recorded

CHECKS = [
    ('s8_scheduled_multi_server_check', s8_scheduled_multi_server_check, 1.5),
]
