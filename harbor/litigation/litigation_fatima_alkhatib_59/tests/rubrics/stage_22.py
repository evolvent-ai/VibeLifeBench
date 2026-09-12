from __future__ import annotations
from ._helpers import *

def s22_pretrial_notes_saved(env) -> bool:
    try:
        return pretrial_notes_saved(env)
    except EvidenceError:
        raise
    except Exception:
        return False

def s22_material_checklist_created(env) -> bool:
    try:
        return material_checklist_created(env)
    except EvidenceError:
        raise
    except Exception:
        return False

CHECKS = [
    ('s22_pretrial_notes_saved', s22_pretrial_notes_saved, 1.5),
    ('s22_material_checklist_created', s22_material_checklist_created, 1.25),
]
