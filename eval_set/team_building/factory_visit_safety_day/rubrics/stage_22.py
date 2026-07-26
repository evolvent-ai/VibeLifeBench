from __future__ import annotations
from ._helpers import *

def s22_late_need_discovered(env) -> bool:
    discovered = notification_has(env, "ntf_013_late_need", ["英文安全提醒需求"])
    acted = used_tool(env, 22, "notification_hub", "list_notifications") and (used_tool(env, 22, "notion") or used_tool(env, 22, "email"))
    return discovered and acted and durable_has(env, [["迟报", "特殊需求"], ["高分贝", "声响", "听力"], ["英文", "双语"], ["复盘", "sop", "整改"]])

CHECKS = [("s22_late_need_discovered", s22_late_need_discovered, 2.5)]
