"""Stage 18 — bindtwo source emails and backend-generated real Meituan application."""
from __future__ import annotations

from ._helpers import (inbox_message_by_id, norm_num, record_text, stage_call_matches,
                       text_has, unique_application_for_job)

MEITUAN_MESSAGE_ID = "<20260720-offer@meituan.com>"
DEWU_MESSAGE_ID = "<20260706-offer@dewu.com>"
JOB_ID = "job_gk_0001"


def _sources_and_application(env) -> dict | None:
    if not stage_call_matches(env, 18, "read_email", {"email_id": "108"}):
        return None
    if not stage_call_matches(env, 18, "read_email", {"email_id": "105"}):
        return None
    if not inbox_message_by_id(env, MEITUAN_MESSAGE_ID) or not inbox_message_by_id(env, DEWU_MESSAGE_ID):
        return None
    return unique_application_for_job(env, JOB_ID, {"offer"})


def s18_offer_compare(env) -> bool:
    app = _sources_and_application(env)
    if not app:
        return False
    app_id = str(app.get("application_id") or "").lower()
    record = record_text(env, "offer_compare.md")
    required = (MEITUAN_MESSAGE_ID.lower(), DEWU_MESSAGE_ID.lower(), app_id, JOB_ID, "job_gk_0007")
    if not all(value in record for value in required):
        return False
    return text_has(record, [
        ["formal Meituan offer", "formal Meituan offer"], ["Dewu"], ["non-binding terms"],
        ["offer", "offer", "offer"], ["stability"], ["standard employee role", "employment"],
        ["non-compete"], ["growth"], ["decision", "decision", "decision"],
    ])


def s18_meituan_offer_value(env) -> bool:
    app = _sources_and_application(env)
    if not app:
        return False
    app_id = str(app.get("application_id") or "").lower()
    record = record_text(env, "offer_compare.md")
    corpus = norm_num(record)
    return all(value in corpus for value in (
        MEITUAN_MESSAGE_ID.lower(), app_id, "32000", "16salaries", "offer", "2026-07-27"
    )) and text_has(record, [["standard employee role"]])


CHECKS = [
    ("s18_offer_compare", s18_offer_compare, 2.5),
    ("s18_meituan_offer_value", s18_meituan_offer_value, 1.5),
]
