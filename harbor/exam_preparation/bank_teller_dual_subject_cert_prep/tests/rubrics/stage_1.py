from __future__ import annotations
from . import _helpers as h


def r03_official_notice_read(env) -> bool:
    return bool(
        h.tool_args_have(env, 1, "notification_hub", "get_account_feed", "acct_bank_exam")
        and h.official_post_seen(env, "post_bank_exam_h2_2026")
        and h.durable_evidence_contains(
            env, "source evidence", "source_evidence.md",
            "2026-07-07", ("官方公告", "考试服务号"), "2026-08-16", "24400",
        )
    )


def r04_dual_subject_rule_recorded(env) -> bool:
    return bool(
        r03_official_notice_read(env)
        and h.durable_evidence_contains(
            env, "subject matrix", "subject_matrix.md",
            "法律法规与综合能力", "专业科目", ("个人理财", "公司信贷", "风险管理"),
        )
    )


CHECKS = [
    ("r03_official_notice_read", r03_official_notice_read, 1.25),
    ("r04_dual_subject_rule_recorded", r04_dual_subject_rule_recorded, 1.5),
]
