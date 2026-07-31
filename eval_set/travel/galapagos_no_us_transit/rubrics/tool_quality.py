from __future__ import annotations

from . import _backend_checks as backend
from ._helpers import (
    called_tool_any_stage,
    count_tool_servers,
    no_forbidden_tools,
    tool_calls_nonredundant,
)


def tool_relevant_server_breadth(env) -> bool:
    return count_tool_servers(env) >= 6 and no_forbidden_tools(env) and backend.persistent_artifacts_complete(env)


def tool_booking_actions_effective(env) -> bool:
    return called_tool_any_stage(env, ["create_booking"], 0, 24) and backend.safe_ticketed_route_complete(env)


def tool_hotel_calendar_actions_effective(env) -> bool:
    return called_tool_any_stage(env, ["create_reservation", "modify_reservation"], 0, 24) and called_tool_any_stage(env, ["create_event", "update_event"], 0, 24) and backend.hotel_authorization_integrity(env) and backend.registration_calendar_ready(env)


def tool_nonredundant_safe_actions(env) -> bool:
    return tool_calls_nonredundant(env) and no_forbidden_tools(env) and backend.all_active_bookings_avoid_us(env)


CHECKS = [
    ("tool_relevant_server_breadth", tool_relevant_server_breadth, 2.0),
    ("tool_booking_actions_effective", tool_booking_actions_effective, 2.0),
    ("tool_hotel_calendar_actions_effective", tool_hotel_calendar_actions_effective, 2.0),
    ("tool_nonredundant_safe_actions", tool_nonredundant_safe_actions, 2.0),
]
