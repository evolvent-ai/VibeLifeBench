from __future__ import annotations
from ._helpers import *

def s6_legal_cases_saved(env) -> bool:
    return tool_used(env, 'legal_search', stage=6) and len(legal_topics_covered(env)) >= 2 and legal_notes_qualified(env, 2)

def s6_legal_route_note_json(env) -> bool:
    return (
        len(legal_topics_covered(env)) >= 2
        and all(
            artifact_has_record(env, 'legal_route_notes.json', groups)
            for groups in [
                [['objection', 'cold', 'near-expiry'], ['source', 'reference', 'court'], ['applicability', 'limitation', 'lawyer']],
                [['signatory', 'electronic', 'carrier'], ['source', 'reference', 'court'], ['applicability', 'limitation', 'lawyer']],
                [['setoff', 'counterclaim', 'paid'], ['source', 'rule', 'case'], ['preparation', 'predict', 'lawyer']],
            ]
        )
    )

CHECKS = [
    ('s6_legal_cases_saved', s6_legal_cases_saved, 1.5),
    ('s6_legal_route_note_json', s6_legal_route_note_json, 1.5),
]
