from __future__ import annotations

from ._helpers import calendar_has, stage_record


def chk_s13_calendar_conflict(env) -> bool:
    backend = calendar_has(env, (("company mandatory safety briefing", "mandatory safety briefing"), ("recovery", "training")))
    logged = stage_record(
        env,
        "calendar_change_log.md",
        13,
        (("briefing",), ("conflict",), ("reschedule", "move"), ("personal training",), ("do not modify company", "read-only")),
        ("Previous window", "New window", "Work/private boundary", "Backend verification"),
    )
    return backend and logged


CHECKS = [("chk_s13_calendar_conflict", chk_s13_calendar_conflict, 1.75)]
