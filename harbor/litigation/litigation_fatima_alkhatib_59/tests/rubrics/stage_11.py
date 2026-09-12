from __future__ import annotations
from ._helpers import *

def s11_recall_law_notes_saved(env) -> bool:
    try:
        return recall_law_notes_saved(env)
    except EvidenceError:
        raise
    except Exception:
        return False

CHECKS = [
    ('s11_recall_law_notes_saved', s11_recall_law_notes_saved, 1.75),
]
