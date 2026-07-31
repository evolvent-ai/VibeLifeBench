from __future__ import annotations
from ._helpers import *


def s23_final_review_written(env) -> bool:
    return (
        closure_archive_refresh(env)
        and stage_record_persisted(
            env,
            23,
            [("首选",), ("备选",), ("淘汰",), ("已核实",), ("待现场",), ("待确认", "本人确认"), ("下一步",)],
            files=("FINAL_REVIEW.md", "CANDIDATE_TRACKER.md", "AUTH_LOG.md"),
        )
    )


def s23_final_refresh_all_core(env) -> bool:
    return (
        closure_archive_refresh(env)
        and late_accessibility_refresh(env)
        and candidate_c_backend_viable(env)
        and stage_record_persisted(
            env,
            23,
            [("状态", "active"), ("路线",), ("邮件", "书面", "合同"), ("评价", "物业", "风险"), ("日程", "待确认"), ("法律", "押金", "服务费")],
            files=("FINAL_REVIEW.md", "CANDIDATE_TRACKER.md", "LEASE_CHECKLIST.md", "AUTH_LOG.md"),
        )
    )


def s23_candidate_matrix_archived(env) -> bool:
    return (
        stage_record_persisted(
            env,
            23,
            [("首选",), ("备选",), ("淘汰",), ("待现场",), ("待确认", "本人确认")],
            files=("FINAL_REVIEW.md", "CANDIDATE_TRACKER.md", "AUTH_LOG.md"),
        )
        and final_candidate_matrix(env)
    )


CHECKS = [
    ('s23_final_review_written', s23_final_review_written, 1.5),
    ('s23_final_refresh_all_core', s23_final_refresh_all_core, 1.75),
    ('s23_candidate_matrix_archived', s23_candidate_matrix_archived, 1.0),
]
