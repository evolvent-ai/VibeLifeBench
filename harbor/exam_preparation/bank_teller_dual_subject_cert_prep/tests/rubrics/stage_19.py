from __future__ import annotations
from . import _helpers as h


def r35_ticket_seat_calendar_updated(env) -> bool:
    return bool(
        h.tool_used(env, 19, "notification_hub")
        and h.tool_used(env, 19, "calendar")
        and h.calendar_ticket_matches_backend(env)
        and h.durable_evidence_contains(env, "exam control", "exam_control.md", "2026-08-16", "3机房", "18号")
    )


CHECKS = [("r35_ticket_seat_calendar_updated", r35_ticket_seat_calendar_updated, 1.75)]
