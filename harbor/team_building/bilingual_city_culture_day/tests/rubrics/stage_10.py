from __future__ import annotations
from ._helpers import *


def s10_access_discovered(env) -> bool:
    return (
        traced_deal_with_status(env, 10, "sold_out")
        and used_tool_with_value(env, 10, "review_platform", "get_deal", ["sold_out", "step-free"])
    )


def s10_access_no_lock(env) -> bool:
    return (
        s10_access_discovered(env)
        and used_tool(env, 10, "email", "save_draft")
        and draft_matches(env, "accessible", "gu.ning", ["sold out", "backup", "do not lock"], stage=10)
        and no_reservation_for_traced_deals(env, 10)
    )


CHECKS = [("s10_access_discovered", s10_access_discovered, 1.75), ("s10_access_no_lock", s10_access_no_lock, 1.25)]
