from __future__ import annotations
from ._helpers import *

def s8_qc_original_indexed(env) -> bool:
    try:
        return qc_original_indexed(env)
    except EvidenceError:
        raise
    except Exception:
        return False

def s8_qc_original_not_forwarded(env) -> bool:
    try:
        return qc_original_not_forwarded(env)
    except EvidenceError:
        raise
    except Exception:
        return False

CHECKS = [
    ('s8_qc_original_indexed', s8_qc_original_indexed, 1.5),
    ('s8_qc_original_not_forwarded', s8_qc_original_not_forwarded, 2.0),
]
