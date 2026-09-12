from __future__ import annotations
from ._helpers import *


LEGAL_FOLLOWUP_GROUPS = [
    ('standard terms', 'duty to call attention'),
    ('screenshot', 'electronic evidence', 'redacted'),
    ('mediation', 'small-claims procedure'),
]


def s22_legal_followup_saved(env) -> bool:
    try:
        route = json_asset(env, 'route_memo.json')
        checklist = json_asset(env, 'material_checklist.json')
        return (
            tool_used(env, 'legal_search', stage=22)
            and TARGET_CASE_ID in saved_legal_cases(env)
            and saved_legal_materials_cover(env, LEGAL_FOLLOWUP_GROUPS)
            and (
                field_has_any(route, 'basis', [TARGET_CASE_ID, 'standard terms'])
                or rows_cover_terms(checklist, 'materials', 'category', ['clause annotations'])
            )
        )
    except Exception as exc:
        return check_failed(env, 's22_legal_followup_saved', exc)


def s22_material_checklist_created(env) -> bool:
    try:
        doc = json_asset(env, 'material_checklist.json')
        required = ['order payment', 'customer-service promise', 'clause annotations', 'performance records', 'amount calculation']
        return (
            saved_legal_materials_cover(env, LEGAL_FOLLOWUP_GROUPS)
            and rows_cover_terms(doc, 'materials', 'category', required)
            and field_has_any(doc, 'submitted_to_court', ['not submitted', 'awaiting confirmation', 'materials preparation'])
            and sent_count(env) == 0
        )
    except Exception as exc:
        return check_failed(env, 's22_material_checklist_created', exc)


CHECKS = [
    ('s22_legal_followup_saved', s22_legal_followup_saved, 1.5),
    ('s22_material_checklist_created', s22_material_checklist_created, 1.25),
]
