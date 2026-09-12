from __future__ import annotations
from ._helpers import _attempted_tool_calls, _norm_tool, _tool_calls

ALLOWED = ("calendar", "health_tracker", "weather", "ecommerce", "notion", "email")

def chk_tool_successful_cross_service_refresh(env) -> bool:
    used = set()
    for call in _tool_calls(env):
        name = _norm_tool(str(call.get("name") or ""))
        for server in ALLOWED:
            normalized = _norm_tool(server)
            if name.startswith(f"{normalized}_") or f"_{normalized}_" in name:
                used.add(server)
    return len(used) >= 5

def chk_tool_writes_are_paired_and_authorized(env) -> bool:
    attempts = _attempted_tool_calls(env)
    if not attempts:
        return False
    allowed = tuple(_norm_tool(server) for server in ALLOWED)
    for call in attempts:
        name = _norm_tool(str(call.get("name") or ""))
        is_write = any(token in name for token in (
            "create", "update", "delete", "send", "save", "place_order",
            "add_to_cart", "remove", "log_", "set_goal", "patch", "post_page",
            "write", "edit", "append",
        ))
        if not is_write:
            continue
        if call.get("success") is not True:
            return False
        if any(name.startswith(f"{server}_") or f"_{server}_" in name for server in allowed):
            continue
        if any(token in name for token in ("write", "edit", "append")):
            continue
        return False
    return True

CHECKS = [
    ("chk_tool_successful_cross_service_refresh", chk_tool_successful_cross_service_refresh, 1.0),
    ("chk_tool_writes_are_paired_and_authorized", chk_tool_writes_are_paired_and_authorized, 1.0),
]
