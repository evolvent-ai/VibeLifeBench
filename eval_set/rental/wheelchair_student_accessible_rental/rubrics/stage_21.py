from __future__ import annotations
from ._helpers import *


def s21_final_email_refresh(env) -> bool:
    return (
        stage21_email_contract_refresh(env)
        and stage21_legal_contract_refresh(env)
        and candidate_c_backend_viable(env)
        and stage_record_persisted(
            env,
            21,
            [("云栖苑", C.LIST_C), ("合同",), ("门宽",), ("服务费",), ("维修",), ("押金",), ("书面", "附件")],
            files=(
                "LEASE_CHECKLIST.md",
                "CANDIDATE_TRACKER.md",
                "RISK_LOG.md",
                "FINAL_REVIEW.md",
                "CONTRACT_QUESTIONS.md",
                "CONTRACT_QA.md",
            ),
        )
    )


def s21_contract_questions_drafted(env) -> bool:
    groups = [
        ("云栖苑",),
        ("合同", "附件"),
        ("门宽",),
        ("服务费",),
        ("维修",),
        ("押金",),
        ("书面", "原件"),
        ("待确认", "待核验", "签约前"),
    ]
    questions_persisted = (
        stage_draft_persisted(env, 21, groups[:-1])
        or stage_record_persisted(
            env,
            21,
            groups,
            files=(
                "LEASE_CHECKLIST.md",
                "CANDIDATE_TRACKER.md",
                "RISK_LOG.md",
                "FINAL_REVIEW.md",
                "CONTRACT_QUESTIONS.md",
                "CONTRACT_QA.md",
            ),
        )
    )
    return s21_final_email_refresh(env) and questions_persisted and no_sent_mail(env)


CHECKS = [
    ('s21_final_email_refresh', s21_final_email_refresh, 1.5),
    ('s21_contract_questions_drafted', s21_contract_questions_drafted, 1.25),
]
