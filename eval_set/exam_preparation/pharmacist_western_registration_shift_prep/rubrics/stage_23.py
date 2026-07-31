from __future__ import annotations

from ._helpers import email_result_seen, stage_calendar_event_written


def r40_second_shift_conflict_moved(env) -> bool:
    return bool(
        email_result_seen(env, 23, "msg_inventory_shift")
        and stage_calendar_event_written(env, 23, date="2026-09-28")
    )


CHECKS = [
    ("r40_second_shift_conflict_moved", r40_second_shift_conflict_moved, 1.5),
]
