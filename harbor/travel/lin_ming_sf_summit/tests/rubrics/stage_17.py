"""Stage 17: notification — client visit."""
from __future__ import annotations
from loguru import logger
from ._helpers import _tool_called_in_stage, _tool_with_args, _call, _ws, _stage_text, _flatten_text, _stage_tools, _trace_successful


def s17_checked_calendar(env) -> bool:
    """Stage 17 called list_events with time range covering 2026-03-29."""
    for tc in _stage_tools(env, 17):
        if not _trace_successful(tc):
            continue
        name = (tc.get("name") or "").lower()
        if "list_events" in name:
            args = tc.get("arguments") or {}
            time_min = str(args.get("time_min", args.get("start", "")))
            time_max = str(args.get("time_max", args.get("end", "")))
            if "2026-03-29" in time_min or "2026-03-28" in time_min or "2026-03-27" in time_min:
                if "2026-03-29" in time_max or "2026-03-30" in time_max or "2026-03-31" in time_max:
                    logger.info("s17_checked_calendar: True")
                    return True
    logger.info("s17_checked_calendar: False")
    return False


def s17_conflict_ack(env) -> bool:
    """The schedule review names both meetings and preserves transfer buffer."""
    text = _stage_text(env, 17).lower()
    plan = _ws(env, "/workspace/trip_plan.md").lower()
    dl = _ws(env, "/workspace/decision_log.md").lower()
    combined = text + "\n" + plan + "\n" + dl
    has_review = any(term in combined for term in ("conflict review", "does not directly overlap", "no direct overlap"))
    has_buffer = "buffer" in combined or "transfer time" in combined
    has_client = "client visit" in combined
    has_standup = "stand-up" in combined
    ok = has_review and has_buffer and has_client and has_standup
    logger.info(f"s17_conflict_ack: review={has_review} buffer={has_buffer} client={has_client} standup={has_standup} -> {ok}")
    return ok


CHECKS = [
    ("s17_checked_calendar", s17_checked_calendar, 1.0),
    ("s17_conflict_ack", s17_conflict_ack, 1.75),
]
