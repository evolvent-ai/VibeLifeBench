from __future__ import annotations

from ._helpers import no_hard_calendar_conflicts, persistent_record


def r33_calendar_audit_no_conflict(env) -> bool:
    return bool(
        no_hard_calendar_conflicts(env)
        and persistent_record(env, 18, "日历", "冲突", "未来两周", min_hits=2)
    )


CHECKS = [
    ("r33_calendar_audit_no_conflict", r33_calendar_audit_no_conflict, 1.5),
]
