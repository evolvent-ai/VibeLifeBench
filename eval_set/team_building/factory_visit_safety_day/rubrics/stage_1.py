from __future__ import annotations
from ._helpers import *

def s1_goal_recorded(env) -> bool:
    read = used_tool(env, 1, "email", "search_emails") or used_tool(env, 1, "email", "get_emails")
    return read and durable_has(env, [["业务理解"], ["安全"], ["自愿", "退出"], ["评审", "审批"]])

CHECKS = [("s1_goal_recorded", s1_goal_recorded, 1.0)]
