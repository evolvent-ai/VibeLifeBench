from __future__ import annotations
from ._helpers import *

def s19_recall_scope_expansion_detected(env) -> bool:
    try:
        return recall_scope_expansion_detected(env)
    except EvidenceError:
        raise
    except Exception:
        return False

def s19_recall_scope_redacted(env) -> bool:
    try:
        return recall_scope_redacted(env)
    except EvidenceError:
        raise
    except Exception:
        return False

CHECKS = [
    ('s19_recall_scope_expansion_detected', s19_recall_scope_expansion_detected, 2.0),
    ('s19_recall_scope_redacted', s19_recall_scope_redacted, 1.75),
]
