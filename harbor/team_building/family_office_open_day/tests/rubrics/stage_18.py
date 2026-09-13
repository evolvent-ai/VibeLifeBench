from __future__ import annotations
from ._helpers import *

def s18_execution_readiness_card(env) -> bool:
    refreshed = sum(1 for server, token in [
        ("ecommerce", "search"), ("ecommerce", "get_cart"),
        ("calendar", "update"), ("maps", "directions"),
        ("review_platform", "get"), ("email", "search"),
    ] if used(env, 18, server, token))
    # event-018 writes "on-site contacts"; has_all is substring-only, so accept
    # the hyphenated spelling the world actually uses.
    recorded = stage_persisted(env, 18, [["onsite", "on-site"], ["visitors", "staggered"], ["allergy", "materials"], ["photography", "fire"]])
    return refreshed >= 2 and recorded

CHECKS = [
    ('s18_execution_readiness_card', s18_execution_readiness_card, 1.5),
]
