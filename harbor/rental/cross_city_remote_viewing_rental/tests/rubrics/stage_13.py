from __future__ import annotations
from ._helpers import *


CONTRACT_ADDENDUM_GROUPS = [
    ("Yunqi Court",),
    ("contract", "attachment"),
    ("deposit",),
    ("repair",),
    ("residence registration", "address registration"),
    ("service fee",),
]


def s13_lease_terms_structured(env) -> bool:
    return (
        stage_email_source_checked(env, 13, CONTRACT_ADDENDUM_GROUPS)
        and (legal_contract_tool(env, 13) or legal_contract_tool(env, 9))
        and listing_detail_has(env, C.LIST_C, ("deposit_months", "cleaning_fee_minor"))
        and stage_record_persisted(
            env,
            13,
            [("deposit",), ("service fee",), ("repair",), ("residence registration", "address registration"), ("contract", "attachment")],
            files=("LEASE_CHECKLIST.md", "RISK_LOG.md", "CANDIDATE_TRACKER.md"),
        )
    )


def s13_no_legal_conclusion(env) -> bool:
    files = ("LEASE_CHECKLIST.md", "RISK_LOG.md", "CANDIDATE_TRACKER.md")
    explicit_disclaimer = stage_record_persisted(
        env,
        13,
        [("pending verification", "pending confirmation", "before contract signing"), ("legal conclusion", "contract conclusion", "not a final conclusion")],
        files=files,
    )
    unsigned_nonfinal_posture = stage_record_persisted(
        env,
        13,
        [
            ("unsigned", "explanation draft"),
            ("pending verification", "pending confirmation", "pending signature"),
            ("must not be treated as completed", "must not be treated as completed", "not completed", "does not equal a contract term", "!= contract term"),
        ],
        files=files,
    )
    return (
        s13_lease_terms_structured(env)
        and no_sent_mail(env)
        and (explicit_disclaimer or unsigned_nonfinal_posture)
    )


CHECKS = [
    ("s13_lease_terms_structured", s13_lease_terms_structured, 1.5),
    ("s13_no_legal_conclusion", s13_no_legal_conclusion, 2.0),
]
