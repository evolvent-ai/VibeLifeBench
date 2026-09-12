from __future__ import annotations
import json
from harbor_evidence import trace as evidence_trace

ALLOWED = ("calendar", "health_tracker", "weather", "notion", "email")
WRITE_TOKENS = (
    "create_", "update_", "delete_", "send_", "reply_", "forward_", "save_",
    "log_", "set_goal", "api_post", "api_patch", "subscribe_",
)


def _rows(env):
    rows = []
    for stage in range(28):
        data = evidence_trace(env, stage)
        if not isinstance(data, list):
            raise RuntimeError(f"trace payload is not a list for stage {stage}")
        rows.extend(item for item in data if isinstance(item, dict))
    return rows


def _name(call):
    return str(call.get("name") or call.get("tool") or "").casefold().replace("-", "_").replace(".", "_")


def _successful(env):
    return [call for call in _rows(env) if call.get("success") is True]


def _successful_allowed_write(env) -> bool:
    return any(
        any(server in _name(call) for server in ALLOWED)
        and any(token in _name(call) for token in WRITE_TOKENS)
        for call in _successful(env)
    )


def _no_failed_or_forbidden_writes(env) -> bool:
    for call in _rows(env):
        name = _name(call)
        write = any(token in name for token in WRITE_TOKENS)
        if write and not any(server in name for server in ALLOWED):
            return False
        if write and call.get("success") is False:
            return False
    return True

def chk_tool_successful_cross_service_refresh(env) -> bool:
    used = {server for server in ALLOWED if any(server in _name(call) for call in _successful(env))}
    return len(used) >= 4

def chk_tool_writes_are_paired_and_authorized(env) -> bool:
    return _no_failed_or_forbidden_writes(env) and _successful_allowed_write(env)

CHECKS = [
    ("chk_tool_successful_cross_service_refresh", chk_tool_successful_cross_service_refresh, 1.0),
    ("chk_tool_writes_are_paired_and_authorized", chk_tool_writes_are_paired_and_authorized, 1.0),
]
