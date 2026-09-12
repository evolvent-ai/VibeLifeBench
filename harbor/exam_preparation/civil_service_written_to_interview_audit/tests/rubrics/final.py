from __future__ import annotations

from ._helpers import check_by_id

def final_handoff_evidence_complete(env) -> bool:
    return check_by_id(env, 'final_handoff_evidence_complete')

CHECKS = [
    ('final_handoff_evidence_complete', final_handoff_evidence_complete, 1.5),
]
