from __future__ import annotations
from . import _helpers as h


def r31_weak_area_calendar_scheduled(env) -> bool:
    return bool(
        h.tool_used(env, 16, "email")
        and h.tool_used(env, 16, "calendar")
        and h.email_message_seen(env, "模考错题回炉建议", "mentor@binjiang-bank.example")
        and h.calendar_has_weak_area_blocks(env)
        and h.durable_evidence_contains(
            env, "wrong question", "wrong_question_ledger.md",
            "反洗钱", "消费者权益保护", "年金现值", "风险匹配", ("安排", "回炉"),
        )
    )


CHECKS = [("r31_weak_area_calendar_scheduled", r31_weak_area_calendar_scheduled, 1.25)]
