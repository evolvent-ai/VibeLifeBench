from __future__ import annotations
from ._helpers import *


def s9_legal_contract_checklist(env) -> bool:
    return (
        legal_contract_tool(env, 9)
        # 服务费来自当前邮件/合同核验链路；房源详情本身只承诺
        # 租赁证明材料与合同资料，不应要求一个不存在的详情字段。
        and listing_detail_has(env, C.LIST_C, ("租赁证明材料", "合同"))
        and stage_structured_evidence(env, 9, ("锁房款", "维修"))
    )


def s9_email_followup_draft(env) -> bool:
    written_questions = (
        stage_draft_has(env, 9, ("服务费",))
        or stage_record_persisted(
            env,
            9,
            [("书面", "问题", "清单"), ("服务费",)],
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
