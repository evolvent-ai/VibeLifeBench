from __future__ import annotations
from ._helpers import *


def s13_credentials_block_lock(env) -> bool:
    return (
        traced_deal_with_status(env, 13, "expired")
        and used_tool_with_value(env, 13, "review_platform", "get_merchant_qa", ["public liability insurance", "bilingual guide credentials", "missing"])
        and used_tool(env, 13, "email", "save_draft")
        and draft_matches(env, "credentials", "gu.ning", ["liability insurance", "credentials", "missing", "do not lock"], stage=13)
        and no_reservation_for_traced_merchants(env, 13)
    )


CHECKS = [("s13_credentials_block_lock", s13_credentials_block_lock, 1.75)]
