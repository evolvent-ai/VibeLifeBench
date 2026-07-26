"""Stage 18 — 绑定两封来源邮件与后端生成的真实 Meituan application。"""
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
        ["美团正式offer", "美团正式 offer"], ["得物"], ["非约束意向条件"],
        ["总包", "32000×16", "512000"], ["稳定"], ["正编", "用工性质"],
        ["竞业"], ["发展"], ["由你自己决定", "由你决定", "你决定"],
    ])


def s18_meituan_offer_value(env) -> bool:
    app = _sources_and_application(env)
    if not app:
        return False
    app_id = str(app.get("application_id") or "").lower()
    record = record_text(env, "offer_compare.md")
    corpus = norm_num(record)
    return all(value in corpus for value in (
        MEITUAN_MESSAGE_ID.lower(), app_id, "32000", "16薪", "512000", "2026-07-27"
    )) and text_has(record, [["正编"]])


CHECKS = [
    ("s18_offer_compare", s18_offer_compare, 2.5),
    ("s18_meituan_offer_value", s18_meituan_offer_value, 1.5),
]
