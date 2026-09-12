from __future__ import annotations
from ._helpers import *

def s6_legal_route_saved(env) -> bool:
    try:
        return legal_route_saved(env)
    except EvidenceError:
        raise
    except Exception:
        return False

def s6_legal_route_json(env) -> bool:
    try:
        return legal_route_json(env)
    except EvidenceError:
        raise
    except Exception:
        return False

def s6_no_legal_certainty(env) -> bool:
    try:
        return no_legal_certainty(env)
    except EvidenceError:
        raise
    except Exception:
        return False

CHECKS = [
    ('s6_legal_route_saved', s6_legal_route_saved, 1.5),
    ('s6_legal_route_json', s6_legal_route_json, 1.5),
    ('s6_no_legal_certainty', s6_no_legal_certainty, 2.0),
]
