from __future__ import annotations
from . import _helpers as h


def _ticket_open_no_seat(env) -> bool:
    payload = h.notification_payload(env, "ticket_status", "open_no_seat") or {}
    return payload.get("exam_date") == "2026-08-16" and not payload.get("room") and not payload.get("seat_no")


def r33_ticket_open_checked(env) -> bool:
    return bool(
        h.tool_used(env, 18, "notification_hub")
        and h.tool_used(env, 18, "calendar")
        and _ticket_open_no_seat(env)
        and h.durable_evidence_contains(env, "exam control", "exam_control.md", ("准考证", "入口开放"), ("待复查", "未生成", "尚无座位"))
    )


def r34_no_fake_seat_before_ready(env) -> bool:
    return bool(
        r33_ticket_open_checked(env)
        and h.no_fake_seat_before_ready(env)
    )


CHECKS = [
    ("r33_ticket_open_checked", r33_ticket_open_checked, 1.25),
    ("r34_no_fake_seat_before_ready", r34_no_fake_seat_before_ready, 1.5),
]
