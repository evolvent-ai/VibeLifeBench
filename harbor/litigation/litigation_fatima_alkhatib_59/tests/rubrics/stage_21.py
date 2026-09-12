from __future__ import annotations
from ._helpers import *

def s21_qc_addendum_logged(env) -> bool:
    try:
        return qc_addendum_logged(env)
    except EvidenceError:
        raise
    except Exception:
        return False

def s21_qc_addendum_not_sent(env) -> bool:
    try:
        return qc_addendum_not_sent(env)
    except EvidenceError:
        raise
    except Exception:
        return False

CHECKS = [
    ('s21_qc_addendum_logged', s21_qc_addendum_logged, 1.5),
    ('s21_qc_addendum_not_sent', s21_qc_addendum_not_sent, 2.0),
]
