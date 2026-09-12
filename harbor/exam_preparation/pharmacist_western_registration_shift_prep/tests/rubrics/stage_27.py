from __future__ import annotations

from ._helpers import ticket_calendar_stage27


def r45_ticket_ready_calendar(env) -> bool:
    return ticket_calendar_stage27(env)


CHECKS = [
    ("r45_ticket_ready_calendar", r45_ticket_ready_calendar, 2.0),
]
