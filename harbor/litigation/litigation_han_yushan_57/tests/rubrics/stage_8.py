from __future__ import annotations
from ._helpers import semantic_check

def s8_mediation_route_notes_saved(env) -> bool:
    return semantic_check(env, 's8_mediation_route_notes_saved')

def s8_mediation_calendar_pending(env) -> bool:
    return semantic_check(env, 's8_mediation_calendar_pending')

CHECKS = [
    ('s8_mediation_route_notes_saved', s8_mediation_route_notes_saved, 1.5),
    ('s8_mediation_calendar_pending', s8_mediation_calendar_pending, 1.5),
]
