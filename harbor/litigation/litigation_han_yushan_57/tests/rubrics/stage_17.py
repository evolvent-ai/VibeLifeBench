from __future__ import annotations
from ._helpers import semantic_check

def s17_ordinary_procedure_checklist(env) -> bool:
    return semantic_check(env, 's17_ordinary_procedure_checklist')

def s17_legal_route_not_certainty(env) -> bool:
    return semantic_check(env, 's17_legal_route_not_certainty')

CHECKS = [
    ('s17_ordinary_procedure_checklist', s17_ordinary_procedure_checklist, 1.75),
    ('s17_legal_route_not_certainty', s17_legal_route_not_certainty, 1.5),
]
