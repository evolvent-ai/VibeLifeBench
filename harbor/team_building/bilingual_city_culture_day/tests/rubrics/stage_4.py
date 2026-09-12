from __future__ import annotations
from ._helpers import *


def s4_review_scan(env) -> bool:
    return (
        used_tool_with_value(env, 4, "review_platform", "search_merchants", ["Guangzhou", "culture"])
        and saved_merchant_from_trace(env, 4)
    )


CHECKS = [("s4_review_scan", s4_review_scan, 1.5)]
