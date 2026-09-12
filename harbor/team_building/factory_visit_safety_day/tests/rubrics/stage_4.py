from __future__ import annotations
from ._helpers import *

def s4_review_scan(env) -> bool:
    return used_tool(env, 4, "review_platform", "search_merchants") and used_tool_with_value(env, 4, "review_platform", "save_merchant", ["mer_7a4c19d2"]) and saved_merchant(env, "mer_7a4c19d2")

CHECKS = [("s4_review_scan", s4_review_scan, 1.5)]
