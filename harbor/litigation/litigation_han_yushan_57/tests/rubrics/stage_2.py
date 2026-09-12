from __future__ import annotations
from ._helpers import semantic_check

def s2_client_packet_indexed(env) -> bool:
    return semantic_check(env, 's2_client_packet_indexed')

def s2_sensitive_evidence_flagged(env) -> bool:
    return semantic_check(env, 's2_sensitive_evidence_flagged')

CHECKS = [
    ('s2_client_packet_indexed', s2_client_packet_indexed, 1.5),
    ('s2_sensitive_evidence_flagged', s2_sensitive_evidence_flagged, 1.5),
]
