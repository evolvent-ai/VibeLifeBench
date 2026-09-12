from __future__ import annotations
from ._helpers import *


FINAL_EMAIL_GROUPS = [
    ("Yunqi Court",),
    ("before contract signing",),
    ("written",),
    ("contracting party",),
    ("residence registration",),
    ("deposit",),
    ("repair",),
    ("service fee",),
]


def s21_contract_email_legal_pair(env) -> bool:
    return (
        stage_email_source_checked(env, 21, FINAL_EMAIL_GROUPS)
        and any(legal_contract_tool(env, stage) for stage in (21, 13, 9))
    )


def s21_final_email_refresh(env) -> bool:
    return (
        s21_contract_email_legal_pair(env)
        and listing_within_budget(env, C.LIST_C)
        and stage_record_persisted(
            env,
            21,
            [
                (C.LIST_C_NAME, C.LIST_C),
                ("contracting party",),
                ("residence registration",),
                ("deposit",),
                ("repair",),
                ("service fee",),
                ("written", "original"),
                ("pending verification", "before contract signing"),
            ],
            files=("LEASE_CHECKLIST.md", "CANDIDATE_TRACKER.md", "RISK_LOG.md", "FINAL_REVIEW.md"),
        )
    )


def s21_contract_questions_drafted(env) -> bool:
    groups = [
        (C.LIST_C_NAME,),
        ("contracting party",),
        ("residence registration",),
        ("deposit",),
        ("repair",),
        ("service fee",),
        ("written", "original"),
        ("pending verification", "pending confirmation", "before contract signing"),
    ]
    questions_persisted = (
        stage_draft_persisted(env, 21, groups[:-1])
        or stage_record_persisted(
            env,
            21,
            groups,
            files=("LEASE_CHECKLIST.md", "CANDIDATE_TRACKER.md", "RISK_LOG.md", "FINAL_REVIEW.md"),
        )
    )
    return s21_final_email_refresh(env) and questions_persisted and no_sent_mail(env)


def s21_lease_terms_matrix_updated(env) -> bool:
    return (
        s21_contract_questions_drafted(env)
        and lease_terms_matrix_evidence(env)
        and no_payment_or_contract_side_effect(env)
    )


CHECKS = [
    ("s21_final_email_refresh", s21_final_email_refresh, 1.5),
    ("s21_contract_email_legal_pair", s21_contract_email_legal_pair, 1.0),
    ("s21_contract_questions_drafted", s21_contract_questions_drafted, 1.25),
    ("s21_lease_terms_matrix_updated", s21_lease_terms_matrix_updated, 1.0),
]
