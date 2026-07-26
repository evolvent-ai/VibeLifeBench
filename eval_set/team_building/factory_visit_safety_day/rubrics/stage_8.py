from __future__ import annotations
from ._helpers import *

def s8_scheduled_monitor(env) -> bool:
    queried = used_tool(env, 8, "review_platform") and used_tool(env, 8, "email") and used_tool(env, 8, "calendar")
    return queried and durable_has(env, [["复查", "监控", "更新"], ["供应商"], ["日历"], ["预算", "风险"]])

CHECKS = [("s8_scheduled_monitor", s8_scheduled_monitor, 1.0)]
