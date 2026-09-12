"""Stage 14: notification — 7-day confirmation."""
from __future__ import annotations
from loguru import logger
from ._helpers import _tool_called_in_stage


def s14_reviewed_status(env) -> bool:
    """Stage 14 called list_bookings AND list_reservations AND list_events."""
    has_bookings = _tool_called_in_stage(env, 14, ["list_bookings"])
    has_reservations = _tool_called_in_stage(env, 14, ["list_reservations"])
    has_events = _tool_called_in_stage(env, 14, ["list_events"])
    ok = has_bookings and has_reservations and has_events
    logger.info(f"s14_reviewed_status: bookings={has_bookings} reservations={has_reservations} events={has_events} -> {ok}")
    return ok


CHECKS = [
    ("s14_reviewed_status", s14_reviewed_status, 1.5),
]
