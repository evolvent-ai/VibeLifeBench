from __future__ import annotations
from . import _helpers as h


def r24_weekly_wrongbook_ready(env) -> bool:
    return bool(
        all(h.tool_used(env, 12, server) for server in ("notification_hub", "calendar", "ecommerce", "notion"))
        and h.durable_evidence_contains(env, "wrong question", "wrong_question_ledger.md", "法律法规", "个人理财", ("待补充", "错题", "回炉"))
        and h.durable_evidence_contains(env, "study plan", "study_plan.md", ("复习", "计划"), ("冲突", "避开"))
        and h.durable_evidence_contains(env, "exam control", "exam_control.md", ("考位", "批次"), ("资料", "正版"), ("报名", "缴费"))
    )


CHECKS = [("r24_weekly_wrongbook_ready", r24_weekly_wrongbook_ready, 1.25)]
