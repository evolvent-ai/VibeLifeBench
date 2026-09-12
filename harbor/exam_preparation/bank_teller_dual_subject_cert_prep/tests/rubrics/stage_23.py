from __future__ import annotations
from . import _helpers as h


def _score_exact(env) -> bool:
    payload = h.notification_payload(env, "score_status", "available") or {}
    return bool(
        payload.get("law_score") == 68
        and payload.get("pf_score") == 72
        and payload.get("passed") is True
        and payload.get("certificate_number") is None
    )


def r41_score_query_after_exam(env) -> bool:
    return bool(
        h.tool_used(env, 23, "notification_hub")
        and _score_exact(env)
        and h.durable_evidence_contains(env, "source evidence", "source_evidence.md", "2026-08-16", ("官方成绩", "成绩通知"))
    )


def r42_scores_recorded_exact(env) -> bool:
    return bool(
        h.tool_used(env, 23, "notification_hub")
        and _score_exact(env)
        and h.durable_evidence_contains(
            env, "final review", "final_review.md",
            "法律法规与综合能力", "68", "个人理财", "72", ("两科通过", "均通过"),
        )
    )


def r43_no_fake_certificate_number(env) -> bool:
    return bool(
        h.tool_used(env, 23, "notification_hub")
        and _score_exact(env)
        and h.final_review_has_no_certificate_number(env)
    )


CHECKS = [
    ("r41_score_query_after_exam", r41_score_query_after_exam, 1.25),
    ("r42_scores_recorded_exact", r42_scores_recorded_exact, 1.5),
    ("r43_no_fake_certificate_number", r43_no_fake_certificate_number, 2.0),
]
