from __future__ import annotations
from ._helpers import *


CONTRACT_ADDENDUM_GROUPS = [
    ("云栖苑",),
    ("合同", "附件"),
    ("押金",),
    ("维修",),
    ("居住登记", "住址登记"),
    ("服务费",),
]


def s13_lease_terms_structured(env) -> bool:
    return (
        stage_email_source_checked(env, 13, CONTRACT_ADDENDUM_GROUPS)
        and (legal_contract_tool(env, 13) or legal_contract_tool(env, 9))
        and listing_detail_has(env, C.LIST_C, ("deposit_months", "cleaning_fee_minor"))
        and stage_record_persisted(
            env,
            13,
            [("押金",), ("服务费",), ("维修",), ("居住登记", "住址登记"), ("合同", "附件")],
            files=("LEASE_CHECKLIST.md", "RISK_LOG.md", "CANDIDATE_TRACKER.md"),
        )
    )


def s13_no_legal_conclusion(env) -> bool:
    files = ("LEASE_CHECKLIST.md", "RISK_LOG.md", "CANDIDATE_TRACKER.md")
    explicit_disclaimer = stage_record_persisted(
        env,
        13,
        [("待核验", "待确认", "签约前"), ("法律结论", "合同结论", "不作最终")],
        files=files,
    )
    unsigned_nonfinal_posture = stage_record_persisted(
        env,
        13,
        [
            ("未签署", "说明稿"),
            ("待核验", "待确认", "待签署"),
            ("不得当作已落实", "不得当已落实", "未落实", "不等于合同条款", "≠ 合同条款"),
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
