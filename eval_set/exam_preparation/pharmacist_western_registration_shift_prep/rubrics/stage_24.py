from __future__ import annotations

from ._helpers import no_hard_calendar_conflicts, persistent_record


def r41_weekly_calendar_audit(env) -> bool:
    return bool(
        no_hard_calendar_conflicts(env)
        and persistent_record(env, 24, "国庆", "休息", "日历", min_hits=2)
    )


CHECKS = [
    ("r41_weekly_calendar_audit", r41_weekly_calendar_audit, 1.5),
]
