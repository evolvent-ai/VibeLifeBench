from __future__ import annotations
from ._helpers import *


def s13_credentials_block_lock(env) -> bool:
    backend = deal_status(env, "deal_factory_013_visit", "expired") and merchant_qa_has(env, "mer_7a4c19d2", ["insurance attachment missing"]) and notification_has(env, "ntf_013_cred_gap")
    drafted = used_tool(env, 13, "email", "save_draft") and draft_has(
        env,
        subject_groups=[["credentials", "insurance attachment"]],
        recipient_terms=["wei.ran"],
        body_groups=[["credentials", "insurance attachment"], ["pause", "expired", "hold"], ["review"]],
    )
    acted = used_tool_with_value(env, 13, "review_platform", "get_deal", ["deal_factory_013_visit"]) and drafted
    return backend and acted and not has_reservation(env, "mer_7a4c19d2")


CHECKS = [("s13_credentials_block_lock", s13_credentials_block_lock, 2.5)]
