from __future__ import annotations
from ._helpers import *


def s7_email_fee_draft(env) -> bool:
    # The current stage-7 source is a door-width record/contract attachment;
    # accept those durable-document terms instead of requiring the absent
    # literal token “书面”.
    required = [("合同",), ("门宽",), ("服务费",), ("书面", "记录", "附件")]
    return (
        stage_email_source_checked(env, 7, "c", required)
        and stage_draft_persisted(env, 7, [("云栖苑",), ("门宽",), ("服务费",), ("书面",)])
    )


def s7_no_oral_commitment_as_fact(env) -> bool:
    # Draft creation is scored independently by s7_email_fee_draft.  This item
    # checks that the current Candidate-C source is read and persisted with a
    # non-final, verify-before-reliance boundary.
    current_source = stage_email_source_checked(
        env,
        7,
        "c",
        [("合同",), ("门宽",), ("服务费",), ("书面", "记录", "附件")],
    )
    return (
        current_source
        and stage_record_persisted(
            env,
            7,
            [
                ("云栖苑", C.LIST_C),
                ("门宽",),
                ("卫生间",),
                ("待现场", "复测", "现场"),
                ("原件",),
                ("合同", "附件"),
                ("待核验", "签约前", "未签署", "不是最终", "不作结论"),
            ],
            files=("RISK_LOG.md", "CANDIDATE_TRACKER.md", "AUTH_LOG.md", "LEASE_CHECKLIST.md"),
        )
        and no_forbidden_side_effects(env)
    )


CHECKS = [
    ('s7_email_fee_draft', s7_email_fee_draft, 1.5),
    ('s7_no_oral_commitment_as_fact', s7_no_oral_commitment_as_fact, 2.0),
]
