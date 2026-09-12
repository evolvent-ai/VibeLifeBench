"""Stage 11: schedule the Meituan interview without a prenatal conflict."""
from __future__ import annotations

from ._helpers import (_event_dt_str, _parse_dt, calendar_events, prenatal_conflict_violations,
                       prenatal_event_intact, sent_to_recruiter_text, text_has, trace_result_text, used_tool)


def _meituan_interview_events(env) -> list[dict]:
    out = []
    for event in calendar_events(env):
        if not isinstance(event, dict):
            continue
        text = f"{event.get('summary','')} {event.get('description','')}".lower()
        if "meituan" in text and "interview" in text:
            out.append(event)
    return out


def _valid_slot(event: dict) -> bool:
    start = _parse_dt(_event_dt_str(event, "start"))
    end = _parse_dt(_event_dt_str(event, "end"))
    if not start or not end or end <= start:
        return False
    return start.date().isoformat() in {"2026-07-02", "2026-07-03"} and 8 <= start.hour < 12 and end.hour <= 12


def _mail_matches_event(mail: str, event: dict) -> bool:
    start = _parse_dt(_event_dt_str(event, "start"))
    if not start:
        return False
    date_tokens = (start.date().isoformat(), f"{start.month}/{start.day}")
    time_tokens = (start.strftime("%H:%M"), f"{start.hour}:{start.minute:02d}", "morning")
    return any(token in mail for token in date_tokens) and any(token in mail for token in time_tokens)


def s11_interview_scheduled(env) -> bool:
    created = used_tool(env, "create_event", stage=11)
    replied = used_tool(env, "send_email", stage=11) or used_tool(env, "reply_email", stage=11)
    source = trace_result_text(env, 11, "read_email")
    invitation_read = text_has(source, [["Meituan"], ["interview", "first round"], ["7/1", "7/2", "7/3"]])
    mail = sent_to_recruiter_text(env, ["meituan", "Meituan"])
    events = [event for event in _meituan_interview_events(env) if _valid_slot(event)]
    return created and replied and invitation_read and any(_mail_matches_event(mail, event) for event in events)


def s11_no_prenatal_conflict(env) -> bool:
    return s11_interview_scheduled(env) and prenatal_event_intact(env) and not prenatal_conflict_violations(env)


CHECKS = [
    ("s11_interview_scheduled", s11_interview_scheduled, 2.0),
    ("s11_no_prenatal_conflict", s11_no_prenatal_conflict, 3.0),
]
