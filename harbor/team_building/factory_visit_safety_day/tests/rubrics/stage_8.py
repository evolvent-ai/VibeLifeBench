from __future__ import annotations
from ._helpers import *

def s8_scheduled_monitor(env) -> bool:
    queried = used_tool(env, 8, "review_platform") and used_tool(env, 8, "email") and used_tool(env, 8, "calendar")
    return queried and durable_has(env, [["follow", "update"], ["supplier"], ["calendar"], ["budget", "risk"]])

CHECKS = [("s8_scheduled_monitor", s8_scheduled_monitor, 1.0)]
