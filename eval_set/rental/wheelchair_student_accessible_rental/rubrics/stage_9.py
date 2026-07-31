from __future__ import annotations
from ._helpers import *


def s9_legal_contract_checklist(env) -> bool:
    return (
        stage_legal_contract_sources_checked(env, 9)
        and stage_record_persisted(
            env,
            9,
            [("合同",), ("押金",), ("门宽",), ("服务费",), ("维修",), ("书面", "附件")],
            files=("LEASE_CHECKLIST.md", "RISK_LOG.md", "LEASE_QUESTIONS.md", "CONTRACT_QUESTIONS.md", "CONTRACT_QA.md"),
        )
    )


def s9_email_followup_draft(env) -> bool:
    groups = [("合同",), ("门宽",), ("服务费",), ("押金",), ("维修",), ("书面", "问题", "清单")]
    written_questions = (
        stage_draft_persisted(env, 9, groups[:-1])
        or stage_record_persisted(
            env,
            9,
            groups,
            files=("LEASE_CHECKLIST.md", "RISK_LOG.md", "LEASE_QUESTIONS.md", "CONTRACT_QUESTIONS.md", "CONTRACT_QA.md"),
        )
    )
    return s9_legal_contract_checklist(env) and written_questions and no_sent_mail(env)


CHECKS = [
    ('s9_legal_contract_checklist', s9_legal_contract_checklist, 1.5),
    ('s9_email_followup_draft', s9_email_followup_draft, 1.25),
]
