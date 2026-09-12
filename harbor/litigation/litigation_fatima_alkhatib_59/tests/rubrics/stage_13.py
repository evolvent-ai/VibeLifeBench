from __future__ import annotations
from ._helpers import *

def s13_recall_mutation_detected(env) -> bool:
    try:
        return recall_mutation_detected(env)
    except EvidenceError:
        raise
    except Exception:
        return False

def s13_recall_watchlist_updated(env) -> bool:
    try:
        return recall_watchlist_updated(env)
    except EvidenceError:
        raise
    except Exception:
        return False

def s13_defense_balanced(env) -> bool:
    try:
        return defense_balanced(env)
    except EvidenceError:
        raise
    except Exception:
        return False

CHECKS = [
    ('s13_recall_mutation_detected', s13_recall_mutation_detected, 2.0),
    ('s13_recall_watchlist_updated', s13_recall_watchlist_updated, 1.5),
    ('s13_defense_balanced', s13_defense_balanced, 1.25),
]
