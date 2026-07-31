"""Stage 11 — 动态绑定真实 application 与后端生成的唯一面试 event。"""
from __future__ import annotations

import datetime

from ._helpers import (calendar_event_details, calendar_events, inbox_message_by_id,
                       prenatal_conflict_violations, prenatal_event_intact,
                       stage_call_matches, stage_calls, unique_application_for_job)

INVITE_MESSAGE_ID = "<20260629-itw@meituan.com>"
JOB_ID = "job_gk_0001"


def _parse(value: str) -> datetime.datetime | None:
    try:
        return datetime.datetime.fromisoformat(value)
    except (TypeError, ValueError):
        return None


def _create_window(env) -> tuple[str, str] | None:
    for call in stage_calls(env, 11, "create_event"):
        args = call.get("arguments") or {}
        start_raw = str(args.get("start") or "")
        end_raw = str(args.get("end") or "")
        start = _parse(start_raw)
        end = _parse(end_raw)
        if not start or not end or end <= start:
            continue
        if not (datetime.date(2026, 7, 1) <= start.date() <= datetime.date(2026, 7, 3)):
            continue
        if not (8 <= start.hour < 12) or end.hour > 13 or end - start > datetime.timedelta(hours=3):
            continue
        return start_raw, end_raw
    return None


def _matching_events(env, application_id: str) -> list[dict]:
    matches = []
    for event in calendar_events(env):
        summary = str(event.get("summary") or "").lower()
        description = str(event.get("description") or "").lower()
        interview_terms = ("面试", "一面", "二面", "三面", "终面")
        if "美团" not in summary or not any(term in summary for term in interview_terms):
            continue
        if JOB_ID not in description or application_id.lower() not in description:
            continue
        details = calendar_event_details(env, str(event.get("event_id") or "")) or event
        matches.append(details)
    return matches


def s11_interview_scheduled(env) -> bool:
    if not stage_call_matches(env, 11, "read_email", {"email_id": "104"}):
        return False
    if not inbox_message_by_id(env, INVITE_MESSAGE_ID):
        return False
    window = _create_window(env)
    app = unique_application_for_job(env, JOB_ID, {"interview", "offer"})
    if not window or not app:
        return False
    app_id = str(app.get("application_id") or "")
    matches = _matching_events(env, app_id)
    if len(matches) != 1:
        return False
    event = matches[0]
    attendees = event.get("attendees") or []
    attendee_ok = any(
        "meituan.com" in str(a.get("email") or "").lower()
        for a in attendees if isinstance(a, dict)
    )
    return (
        attendee_ok
        and str(event.get("start") or "") == window[0]
        and str(event.get("end") or "") == window[1]
        and str(event.get("status") or "").lower() == "confirmed"
    )


def s11_no_prenatal_conflict(env) -> bool:
    return s11_interview_scheduled(env) and prenatal_event_intact(env) and not prenatal_conflict_violations(env)


CHECKS = [
    ("s11_interview_scheduled", s11_interview_scheduled, 2.0),
    ("s11_no_prenatal_conflict", s11_no_prenatal_conflict, 2.5),
]
