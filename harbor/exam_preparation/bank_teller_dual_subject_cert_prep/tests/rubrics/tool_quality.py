from __future__ import annotations
from . import _helpers as h

EXPECTED_SERVICES = ("banking", "calendar", "ecommerce", "email", "notification_hub", "notion")


def _successful_calls(env):
    return [call for call in h.trace_calls(env) if call.get("success") is True]


def _call_name(call) -> str:
    return str(call.get("name") or "").casefold().replace("-", "_")


def tq_successful_tool_result_coverage(env) -> bool:
    calls = _successful_calls(env)
    stages = {call.get("_stage") for call in calls if isinstance(call.get("_stage"), int)}
    return len(calls) >= 25 and len(stages) >= 18


def tq_required_service_coverage(env) -> bool:
    calls = _successful_calls(env)
    return all(sum(1 for call in calls if server in _call_name(call)) >= 2 for server in EXPECTED_SERVICES)


CHECKS = [
    ("tq_successful_tool_result_coverage", tq_successful_tool_result_coverage, 1.5),
    ("tq_required_service_coverage", tq_required_service_coverage, 1.5),
]
