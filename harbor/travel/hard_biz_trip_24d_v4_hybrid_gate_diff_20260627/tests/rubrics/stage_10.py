"""Stage 10: meeting conflict - email, calendar, reasoning, and unsent draft."""
from __future__ import annotations
from loguru import logger
from ._helpers import _any, _has_email_draft_target, _stage_email_draft_text, _agent_used_tool, _workspace_file_text, _calendar_conflict_backend


def s10_checked_email(env) -> bool:
    ok = _agent_used_tool(env, "email", "search_emails", stage=10) or _agent_used_tool(env, "email", "read_email", stage=10)
    logger.info(f"s10_email: {ok}"); return ok


def s10_checked_calendar(env) -> bool:
    used = _agent_used_tool(env, "calendar", "list_events", stage=10) or _agent_used_tool(env, "calendar", "get_event", stage=10)
    ok = used and _calendar_conflict_backend(env)
    logger.info(f"s10_cal_backend: {ok}"); return ok


def s10_detected_conflict(env) -> bool:
    text = _workspace_file_text(env, "/workspace/decision_log.md").lower()
    described = _any(text, ["conflict", "overlap", "reschedule", "keynote", "14:00"]) and _any(text, ["7/20", "jul 20", "20th"])
    ok = described and _calendar_conflict_backend(env)
    logger.info(f"s10_conflict_backend: {ok}"); return ok


def s10_proposed_solution(env) -> bool:
    draft = _stage_email_draft_text(env, 10)
    not_sent = not _agent_used_tool(env, "email", "send_email", stage=10)
    correct_thread = _has_email_draft_target(env, "tanaka@abc.example", stage=10, in_reply_to="<client-meeting-20260716@abc.example>")
    content = _any(draft, ["reschedule", "alternative", "morning", "after the meeting"]) and _any(draft, ["summit", "conference", "keynote", "conflict"])
    ok = bool(draft.strip()) and not_sent and correct_thread and content and _calendar_conflict_backend(env)
    logger.info(f"s10_solution: {ok}"); return ok


CHECKS = [("s10_checked_email", s10_checked_email, 1.5), ("s10_checked_calendar", s10_checked_calendar, 1.5), ("s10_detected_conflict", s10_detected_conflict, 2.0), ("s10_proposed_solution", s10_proposed_solution, 1.5)]
