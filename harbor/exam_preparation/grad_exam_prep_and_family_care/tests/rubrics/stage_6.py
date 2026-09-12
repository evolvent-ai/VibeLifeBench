from __future__ import annotations
from ._helpers import *

def r13_read_reschedule(env) -> bool:
    try:
        text = _agent_reply(env, 6) + "\n" + _trace_text(env, 6, 6) + "\n" + _emails_text(env)
        return (
            _stage_trace_all(env, 6, [["email", "mail"], ["read_email", "search_emails", "get_emails"]])
            and any_has(text, ["11-29", "11 month29", "29morning"])
            and any_has(text, ["Dr. Wang", "follow-up", "reschedule"])
        )
    except Exception:
        return False

def r14_move_visit(env) -> bool:
    try:
        text = _agent_reply(env, 6) + "\n" + _trace_text(env, 6, 7) + "\n" + wfile(env, "CONTROL_CENTER.md")
        return (
            _stage_trace_all(env, 6, [["calendar", "event"], ["update_event", "create_event", "delete_event"]])
            and any_has(text, ["11-29", "11 month29", "hospitalfollow-up", "follow-up"])
            and any_has(text, ["reschedule", "move", "move aside", "split"])
            and _calendar_event_count(env, [["11-29", "2026-11-29", "11 month29"], ["follow-up", "Ms. Li", "knee"]]) >= 1
            and _calendar_event_count(env, [["rest", "split"], ["incorrect", "problems", "Math"]]) >= 1
            and _calendar_event_count(env, [["2026-11-28"], ["Ms. Li", "follow-up"]]) == 0
            and calendar_has_no_long_study_blocks(env)
        )
    except Exception:
        return False

def r15_calendar_no_4h_violate(env) -> bool:
    try:
        return (
            calendar_has_no_long_study_blocks(env)
            and _valid_full_length_mock_events(env, 4)
            and _calendar_event_count(env, [["2026-11-29"], ["Ms. Li", "follow-up", "knee"]]) >= 1
            and _calendar_event_count(env, [["rest", "break"], ["Math", "incorrect", "problems", "mock"]]) >= 2
            and _calendar_event_count(env, [["full-length", "mock", "mock"]]) >= 4
            and _notion_has(env, [["11-29", "2026-11-29", "11 month29"], ["follow-up", "Dr. Wang"], ["4 hours", "rest", "split"]])
        )
    except Exception:
        return False

CHECKS = [
    ("r13_read_reschedule", r13_read_reschedule, 3.0),
    ("r14_move_visit", r14_move_visit, 4.0),
    ("r15_calendar_no_4h_violate", r15_calendar_no_4h_violate, 5.0),
]
