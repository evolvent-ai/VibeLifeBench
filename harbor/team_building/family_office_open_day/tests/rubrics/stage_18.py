from __future__ import annotations
from ._helpers import *

def s18_execution_readiness_card(env) -> bool:
    refreshed = sum(1 for server, token in [
        ("ecommerce", "search"), ("ecommerce", "get_cart"),
        ("calendar", "update"), ("maps", "directions"),
        ("review_platform", "get"), ("email", "search"),
    ] if used(env, 18, server, token))
    recorded = stage_persisted(env, 18, [["onsite"], ["visitors", "staggered"], ["allergy", "materials"], ["photography", "fire"]])
    return refreshed >= 2 and recorded

CHECKS = [
    ('s18_execution_readiness_card', s18_execution_readiness_card, 1.5),
]
