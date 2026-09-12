from __future__ import annotations
from ._helpers import *

def s4_workshop_credentials_draft(env) -> bool:
    route_checked = used_any(env, 4, [("maps", "search"), ("maps", "directions"), ("maps", "get_place")])
    recorded = stage_persisted(env, 4, [["office", "entrance"], ["backup", "assembly"], ["freight"], ["server", "Finance", "fire"]])
    return route_checked and recorded

CHECKS = [
    ('s4_workshop_credentials_draft', s4_workshop_credentials_draft, 1.5),
]
