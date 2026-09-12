from __future__ import annotations
from ._helpers import *

def s4_legal_letter_indexed(env) -> bool:
    try:
        return legal_letter_indexed(env)
    except EvidenceError:
        raise
    except Exception:
        return False

def s4_no_admission_after_claim(env) -> bool:
    try:
        return no_admission_after_claim(env)
    except EvidenceError:
        raise
    except Exception:
        return False

CHECKS = [
    ('s4_legal_letter_indexed', s4_legal_letter_indexed, 1.25),
    ('s4_no_admission_after_claim', s4_no_admission_after_claim, 1.75),
]
