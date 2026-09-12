from __future__ import annotations
from ._helpers import *


def s7_legal_format_notes_saved(env) -> bool:
    try:
        return TARGET_CASE_ID in saved_legal_cases(env)
    except Exception as exc:
        return check_failed(env, 's7_legal_format_notes_saved', exc)

def s7_legal_route_note_json(env) -> bool:
    try:
        doc = json_asset(env, 'route_memo.json')
        return field_is_false(doc, 'legal_advice') and field_is_true(doc, 'materials_only')
    except Exception as exc:
        return check_failed(env, 's7_legal_route_note_json', exc)

CHECKS = [
    ('s7_legal_format_notes_saved', s7_legal_format_notes_saved, 1.5),
    ('s7_legal_route_note_json', s7_legal_route_note_json, 1.25),
]
