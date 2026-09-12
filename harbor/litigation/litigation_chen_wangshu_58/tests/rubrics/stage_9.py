from __future__ import annotations
from ._helpers import *


def s9_core_clauses_annotated(env) -> bool:
    try:
        doc = json_asset(env, 'clause_annotations.json')
        return (
            bool(terms_email(env))
            and TARGET_CASE_ID in saved_legal_cases(env)
            and rows_cover_terms(doc, 'clauses', 'category', ['no refund after classes begin', 'standard terms', 'installment payment', 'training credits'])
        )
    except Exception as exc:
        return check_failed(env, 's9_core_clauses_annotated', exc)


def s9_clause_sources_bound(env) -> bool:
    try:
        doc = json_asset(env, 'clause_annotations.json')
        rows = list_from_doc(doc, 'clauses')
        required = ['no refund after classes begin', 'standard terms', 'installment payment', 'training credits']
        bound = all(
            any(
                row_field_has(row, 'category', term)
                and bool(flatten_struct(get_value(row, 'source', '')).strip())
                and field_has_any(row, 'issue_tag', ['refund', 'call attention', 'installment', 'substitute', 'promise'])
                and field_has_any(row, 'basis', ['Civil Code', 'consumer', 'standard terms', TARGET_CASE_ID])
                for row in rows
            )
            for term in required
        )
        source_text = flatten_struct([get_value(row, 'source', '') for row in rows])
        multi_source = (
            any(term in source_text for term in ['service agreement', 'attachment'])
            and any(term in source_text for term in ['customer service', 'email', 'order', 'page'])
            and any(term in source_text for term in ['legal', 'case', 'Civil Code', 'consumer'])
        )
        return bound and multi_source and bool(terms_email(env)) and TARGET_CASE_ID in saved_legal_cases(env)
    except Exception as exc:
        return check_failed(env, 's9_clause_sources_bound', exc)


CHECKS = [
    ('s9_core_clauses_annotated', s9_core_clauses_annotated, 1.75),
    ('s9_clause_sources_bound', s9_clause_sources_bound, 1.5),
]
