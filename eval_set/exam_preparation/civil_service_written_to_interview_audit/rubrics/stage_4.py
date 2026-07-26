from __future__ import annotations

from ._helpers import check_by_id

def stage_04_legal_directory_checked(env) -> bool:
    return check_by_id(env, 'stage_04_legal_directory_checked')

def stage_04_source_evidence_extended(env) -> bool:
    return check_by_id(env, 'stage_04_source_evidence_extended')

CHECKS = [
    ('stage_04_legal_directory_checked', stage_04_legal_directory_checked, 1.75),
    ('stage_04_source_evidence_extended', stage_04_source_evidence_extended, 1.5),
]
