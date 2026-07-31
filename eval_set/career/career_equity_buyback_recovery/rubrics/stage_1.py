"""Stage 1 — 读取并登记初始 HR 通知。"""
from __future__ import annotations

from ._helpers import inbox_message_by_id, record_text, stage_call_matches, text_has

NOTICE_MESSAGE_ID = "<hr-notice@yiweicloud.com>"


def s1_notice_logged(env) -> bool:
    if not stage_call_matches(env, 1, "read_email", {"email_id": "1"}):
        return False
    message = inbox_message_by_id(env, NOTICE_MESSAGE_ID)
    if not message:
        return False
    record = record_text(env, "severance_review.md")
    return text_has(record, [[NOTICE_MESSAGE_ID], ["第四十条", "第40条"], ["2026-06-30"]])


CHECKS = [("s1_notice_logged", s1_notice_logged, 2.0)]
