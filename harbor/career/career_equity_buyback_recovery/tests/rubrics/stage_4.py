"""Stage 4 — read and log the company proposal."""
from __future__ import annotations

from ._helpers import has_values, inbox_message_by_id, record_text, stage_call_matches, text_has

PLAN_MESSAGE_ID = "<20260615-plan@yiweicloud.com>"


def s4_plan_logged(env) -> bool:
    if not stage_call_matches(env, 4, "read_email", {"email_id": "101"}):
        return False
    message = inbox_message_by_id(env, PLAN_MESSAGE_ID)
    if not message:
        return False
    record = record_text(env, "severance_review.md")
    return PLAN_MESSAGE_ID.lower() in record and has_values(record, "200100") and text_has(
        record, [["internal fixed price", "fixed price"], ["2026-06-22", "June 22", "6/22"]]
    )


CHECKS = [("s4_plan_logged", s4_plan_logged, 1.5)]
