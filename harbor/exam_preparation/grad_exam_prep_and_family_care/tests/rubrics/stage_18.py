from __future__ import annotations
from ._helpers import *

def r29_syllabus_update(env) -> bool:
    try:
        text = _agent_reply(env, 18) + "\n" + _trace_text(env, 18, 18) + "\n" + wfile(env, "CONTROL_CENTER.md") + "\n" + _emails_text(env)
        return (
            _stage_trace_all(env, 18, [["email", "mail", "messages"], ["read_email", "search_emails", "get_emails"], ["api-", "notion"], ["api-get-block-children", "api-post-database-query"]])
            and any_has(text, ["partial-differential", "analytic geometry", "applications"])
            and any_has(text, ["stochastic-process", "new topics", "syllabus", "supplement", "concepts", "basic"])
            and _notion_has(env, [["partial-differential", "applications"], ["analytic geometry"], ["stochastic-process", "concepts"], ["new topics", "syllabus", "supplement", "notice"]])
            and _stage_reply_has(env, 18, [["partial-differential"], ["analytic geometry"], ["stochastic-process"], ["preview", "1-2 hours", "1 hour", "2 hours", "according"]])
        )
    except Exception:
        return False

def r30_calendar_syllabus_review(env) -> bool:
    try:
        text = _agent_reply(env, 18) + "\n" + _trace_text(env, 18, 18) + "\n" + wfile(env, "CONTROL_CENTER.md") + "\n" + _calendar_text(env)
        return (
            _stage_trace_all(env, 18, [["calendar", "event"], ["create_event", "update_event"]])
            and any_has(text, ["1-2", "preview", "new topics"])
            and any_has(text, ["partial-differential", "stochastic-process", "analytic geometry"])
            and _calendar_has(env, [["new topics", "syllabus", "preview"], ["partial-differential", "stochastic-process", "analytic geometry"], ["1-2"]])
            and _calendar_event_count(env, [["partial-differential"], ["preview", "new topics"]]) >= 1
            and _calendar_event_count(env, [["stochastic-process"], ["preview", "new topics"]]) >= 1
            and calendar_has_no_long_study_blocks(env)
        )
    except Exception:
        return False

CHECKS = [
    ("r29_syllabus_update", r29_syllabus_update, 3.0),
    ("r30_calendar_syllabus_review", r30_calendar_syllabus_review, 3.0),
]
