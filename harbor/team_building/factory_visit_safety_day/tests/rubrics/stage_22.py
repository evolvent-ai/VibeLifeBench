from __future__ import annotations
from ._helpers import *

def s22_late_need_discovered(env) -> bool:
    discovered = notification_has(env, "ntf_013_late_need", ["English safety reminder request"])
    acted = used_tool(env, 22, "notification_hub", "list_notifications") and (used_tool(env, 22, "notion") or used_tool(env, 22, "email"))
    return discovered and acted and durable_has(env, [["late", "special"], ["noise", "hearing"], ["English"], ["retrospective", "SOP"]])

CHECKS = [("s22_late_need_discovered", s22_late_need_discovered, 2.5)]
