"""Stage 4: calendar - backend events and durable itinerary must agree."""
from __future__ import annotations
from loguru import logger
from ._helpers import (
    _any,
    _agent_used_tool,
    _call,
    _tool_calls,
    _tool_name_matches,
    _workspace_file_text,
)


def _created_calendar_arguments(env) -> list[dict]:
    return [
        dict(call.get("arguments") or {})
        for call in _tool_calls(env, 4)
        if _tool_name_matches(str(call.get("name") or ""), "calendar", "create_event")
        and isinstance(call.get("arguments"), dict)
    ]


def _event_start(item: dict) -> str:
    # create_event arguments carry a plain "start" string, while the calendar
    # mock persists events with a nested {"dateTime": ...} (or {"date": ...}
    # for all-day rows); unwrap the dict before the date-prefix comparisons.
    value = item.get("start_dt") or item.get("start")
    if isinstance(value, dict):
        value = value.get("dateTime") or value.get("datetime") or value.get("date")
    return str(value or "")


def _event_summary(item: dict) -> str:
    return str(item.get("summary") or item.get("title") or "").lower()


def _role_match(item: dict, date: str, words: list[str]) -> bool:
    text = "\n".join([
        _event_summary(item),
        str(item.get("description") or "").lower(),
    ])
    return _event_start(item).startswith(date) and _any(text, words)


def _persisted_created_role(items: list[dict], calls: list[dict], date: str, words: list[str]) -> bool:
    matching_calls = [call for call in calls if _role_match(call, date, words)]
    if not matching_calls:
        return False
    for call in matching_calls:
        call_summary = _event_summary(call)
        if any(
            isinstance(item, dict)
            and str(item.get("status") or "confirmed").lower() == "confirmed"
            and _event_start(item).startswith(date)
            and _event_summary(item) == call_summary
            for item in items
        ):
            return True
    return False

def s4_backend_events_exist(env) -> bool:
    """Five successful create calls must persist as five distinct business events."""
    events = _call(env, "calendar", "list_events")
    if isinstance(events, dict):
        items = events.get("events") or events.get("items") or []
    elif isinstance(events, list):
        items = events
    else:
        items = []
    calls = _created_calendar_arguments(env)
    roles = [
        ("2026-07-13", ["reminder", "organize", "luggage"]),
        ("2026-07-15", ["depart", "departure", "set off"]),
        ("2026-07-20", ["summit", "conference", "meeting"]),
        ("2026-07-21", ["summit", "conference", "meeting"]),
        ("2026-07-22", ["return", "return trip", "return home"]),
    ]
    persisted_roles = [
        _persisted_created_role(items, calls, date, words)
        for date, words in roles
    ]
    distinct_starts = {str(call.get("start") or call.get("start_dt") or "")[:10] for call in calls}
    ok = len(calls) >= 5 and len(distinct_starts) >= 5 and all(persisted_roles)
    logger.info(
        f"s4_backend: backend_n={len(items)} successful_creates={len(calls)} "
        f"distinct_dates={len(distinct_starts)} roles={persisted_roles} -> {ok}"
    )
    return ok

def s4_tool_used(env) -> bool:
    # The calendar service exposes create_event but has no send_invite tool.
    # Successful creation is the observable action required at this stage.
    ok = _agent_used_tool(env, "calendar", "create_event", stage=4)
    logger.info(f"s4_tool: {ok}")
    return ok

def s4_reply_lists_dates(env) -> bool:
    """The durable itinerary names departure, summit days, return, and reminder."""
    text = _workspace_file_text(env, "/workspace/itinerary.md").lower()
    has_depart = _any(text, ["depart", "departure", "7/15", "july 15", "15th"])
    has_conf1 = _any(text, ["summit", "conference", "7/20", "july 20", "20th", "day 1", "day1"])
    has_conf2 = _any(text, ["7/21", "july 21", "21st", "day 2", "day2", "second"])
    has_return = _any(text, ["return", "return trip", "7/22", "july 22", "22nd"])
    has_reminder = _any(text, ["7/13", "july 13", "13th", "two days before", "reminder"])
    ok = has_depart and has_conf1 and has_conf2 and has_return and has_reminder
    logger.info(f"s4_list: depart={has_depart} d1={has_conf1} d2={has_conf2} ret={has_return} reminder={has_reminder} -> {ok}")
    return ok

CHECKS = [
    ("s4_backend_events_exist", s4_backend_events_exist, 2.0),
    ("s4_tool_used", s4_tool_used, 1.0),
    ("s4_reply_lists_dates", s4_reply_lists_dates, 2.0),
]
