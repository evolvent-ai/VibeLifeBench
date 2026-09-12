from __future__ import annotations
from ._helpers import wfile, audit_tx_count

def s23_deep_audit_0(env) -> bool:
    text = wfile(env, 'audit_journal.md')
    if not text or not text.strip():
        return False
    return audit_tx_count(env, text.lower()) >= 6
CHECKS = [('s23_deep_audit_0', s23_deep_audit_0, 3.0)]
