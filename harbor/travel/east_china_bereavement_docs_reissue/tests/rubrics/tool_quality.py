from __future__ import annotations

from ._helpers import (
    check_tool_booking_actions_effective,
    check_tool_nonredundant_safe_actions,
    check_tool_persistence_actions_effective,
    check_tool_relevant_server_breadth,
)


def tool_relevant_server_breadth(env) -> bool:
    return check_tool_relevant_server_breadth(env)


def tool_booking_actions_effective(env) -> bool:
    return check_tool_booking_actions_effective(env)


def tool_persistence_actions_effective(env) -> bool:
    return check_tool_persistence_actions_effective(env)


def tool_nonredundant_safe_actions(env) -> bool:
    return check_tool_nonredundant_safe_actions(env)


CHECKS = [
    ("tool_relevant_server_breadth", tool_relevant_server_breadth, 2.0),
    ("tool_booking_actions_effective", tool_booking_actions_effective, 2.0),
    ("tool_persistence_actions_effective", tool_persistence_actions_effective, 2.0),
    ("tool_nonredundant_safe_actions", tool_nonredundant_safe_actions, 2.0),
]
