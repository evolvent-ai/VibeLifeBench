from __future__ import annotations
from ._helpers import *

def s21_legal_refresh_saved(env) -> bool:
    return legal_topics_covered(env) == {'quality', 'delivery', 'offset'} and legal_notes_qualified(env, 3, query_date='2026-08-24')

def s21_legal_late_rechecked(env) -> bool:
    return (
        tool_used(env, 'legal_search', 'search_cases', stage=21)
        and tool_used(env, 'legal_search', 'add_note_to_case', stage=21)
        and legal_topics_covered(env) == {'quality', 'delivery', 'offset'}
        and legal_notes_qualified(env, 3, query_date='2026-08-24')
    )

CHECKS = [
    ('s21_legal_refresh_saved', s21_legal_refresh_saved, 1.5),
    ('s21_legal_late_rechecked', s21_legal_late_rechecked, 1.0),
]
