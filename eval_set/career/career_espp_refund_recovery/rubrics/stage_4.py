"""Stage 4 — 读取并登记公司低价方案。"""
from __future__ import annotations

from ._helpers import inbox_message_by_id, norm_num, record_text, stage_call_matches, text_has

PLAN_MESSAGE_ID = "<20260615-plan@ximingsemi.com>"


def s4_plan_logged(env) -> bool:
    if not stage_call_matches(env, 4, "read_email", {"email_id": "101"}):
        return False
    message = inbox_message_by_id(env, PLAN_MESSAGE_ID)
    if not message:
        return False
    record = record_text(env, "severance_review.md")
    return PLAN_MESSAGE_ID.lower() in record and "200300" in norm_num(record) and text_has(
        record, [["内部固定价", "固定价"], ["2026-06-22", "6月22", "6/22"]]
    )


CHECKS = [("s4_plan_logged", s4_plan_logged, 1.5)]
