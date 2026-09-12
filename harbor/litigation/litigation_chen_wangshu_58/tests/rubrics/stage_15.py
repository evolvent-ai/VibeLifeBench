from __future__ import annotations
from ._helpers import *


def s15_installment_statement_rechecked(env) -> bool:
    try:
        doc = json_asset(env, 'installment_dispute.json')
        expected = installment_fee_total(env)
        return tool_used(env, 'credit_card', stage=15) and expected > 0 and numeric_eq(doc, 'fee_total_minor', expected)
    except Exception as exc:
        return check_failed(env, 's15_installment_statement_rechecked', exc)

def s15_platform_complaint_draft_saved(env) -> bool:
    try:
        doc = json_asset(env, 'academy_complaint.json')
        draft_recorded = (
            field_is_true(doc, 'draft_saved')
            or field_has_any(doc, 'draft_saved', ['saved', 'draft', 'not sent', 'awaiting confirmation'])
        )
        return (
            draft_count(env) >= 1
            and (tool_used(env, 'email', 'save_draft', stage=15) or draft_recorded)
        )
    except Exception as exc:
        return check_failed(env, 's15_platform_complaint_draft_saved', exc)

def s15_complaint_not_sent(env) -> bool:
    try:
        doc = json_asset(env, 'academy_complaint.json')
        return sent_count(env) == 0 and field_has_any(doc, 'draft_saved', ['not sent', 'awaiting confirmation', 'draft'])
    except Exception as exc:
        return check_failed(env, 's15_complaint_not_sent', exc)

CHECKS = [
    ('s15_installment_statement_rechecked', s15_installment_statement_rechecked, 1.5),
    ('s15_platform_complaint_draft_saved', s15_platform_complaint_draft_saved, 1.5),
    ('s15_complaint_not_sent', s15_complaint_not_sent, 2.0),
]
