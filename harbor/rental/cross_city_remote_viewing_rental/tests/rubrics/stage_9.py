from __future__ import annotations
from ._helpers import *


def s9_legal_contract_checklist(env) -> bool:
    return (
        legal_contract_tool(env, 9)
        # service fee from the current email/contract verification chain;the listing detail itself only promises
        # Lease proof and contract materials must not require a nonexistent detail field.
        and listing_detail_has(env, C.LIST_C, ("lease proof documents", "contract"))
        and stage_structured_evidence(env, 9, ("holding fee", "repair"))
    )


def s9_email_followup_draft(env) -> bool:
    written_questions = (
        stage_draft_has(env, 9, ("service fee",))
        or stage_record_persisted(
            env,
            9,
            [("written", "question", "checklist"), ("service fee",)],
            files=(
                "VERIFICATION_QUESTIONS.md",
                "WRITTEN_QUESTIONS.md",
                "LEASE_CHECKLIST.md",
                "RISK_LOG.md",
            ),
        )
    )
    return s9_legal_contract_checklist(env) and written_questions and no_sent_mail(env)


CHECKS = [
    ("s9_legal_contract_checklist", s9_legal_contract_checklist, 1.5),
    ("s9_email_followup_draft", s9_email_followup_draft, 1.25),
]
