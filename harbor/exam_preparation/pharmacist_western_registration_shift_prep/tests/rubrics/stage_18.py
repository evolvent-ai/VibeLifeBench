from __future__ import annotations

from ._helpers import no_hard_calendar_conflicts, persistent_record


def r33_calendar_audit_no_conflict(env) -> bool:
    return bool(
        no_hard_calendar_conflicts(env)
        and persistent_record(env, 18, "calendar", "conflict", "next two weeks", min_hits=2)
    )


CHECKS = [
    ("r33_calendar_audit_no_conflict", r33_calendar_audit_no_conflict, 1.5),
]
