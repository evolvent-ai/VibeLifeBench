from __future__ import annotations
from ._helpers import *


def s2_promise_email_indexed(env) -> bool:
    try:
        doc = json_asset(env, 'promise_evidence.json')
        row = row_matching(doc, 'evidence', 'category', 'trial period', 'promise')
        email = promise_email(env)
        return (
            tool_used(env, 'email', stage=2)
            and bool(email)
            and bool(row)
            and row_references_email(row, email)
            and row_field_has(row, 'sensitivity', 'medium', 'high', 'medium', 'high')
        )
    except Exception as exc:
        return check_failed(env, 's2_promise_email_indexed', exc)


def s2_promise_not_overstated(env) -> bool:
    try:
        doc = json_asset(env, 'promise_evidence.json')
        row = row_matching(doc, 'evidence', 'category', 'trial period', 'promise')
        return bool(
            promise_email(env)
            and row
            and row_field_has(row, 'legal_status', 'evidence', 'awaiting verification')
            and row_field_false(row, 'approved_refund')
        )
    except Exception as exc:
        return check_failed(env, 's2_promise_not_overstated', exc)


CHECKS = [
    ('s2_promise_email_indexed', s2_promise_email_indexed, 1.5),
    ('s2_promise_not_overstated', s2_promise_not_overstated, 1.25),
]
