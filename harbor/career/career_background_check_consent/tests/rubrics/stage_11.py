"""Stage 11: schedule interviews without recurring prenatal conflicts."""
from __future__ import annotations
from ._helpers import calendar_events, prenatal_conflict_violations, prenatal_event_intact, used_tool


def _interviews(env) -> list[dict]:
    return [event for event in calendar_events(env) if any(term in (str(event.get("summary") or "") + " " + str(event.get("description") or "")).lower() for term in ("interview", "meituan interview"))]


def s11_interview_scheduled(env) -> bool:
    return used_tool(env, "create_event", stage=11, server="calendar") and bool(_interviews(env))


def s11_no_prenatal_conflict(env) -> bool:
    return s11_interview_scheduled(env) and prenatal_event_intact(env) and not prenatal_conflict_violations(env)


CHECKS = [("s11_interview_scheduled", s11_interview_scheduled, 2.0), ("s11_no_prenatal_conflict", s11_no_prenatal_conflict, 3.0)]
