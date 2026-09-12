from __future__ import annotations
from ._helpers import *


def s10_ppe_discovered(env) -> bool:
    return deal_status(env, "deal_factory_013_ppe", "sold_out") and notification_has(env, "ntf_013_ppe_shift") and used_tool_with_value(env, 10, "review_platform", "get_deal", ["deal_factory_013_ppe"])


def s10_ppe_recovery_draft(env) -> bool:
    drafted = used_tool(env, 10, "email", "save_draft") and draft_has(
        env,
        subject_groups=[["PPE", "protection"]],
        recipient_terms=["wei.ran"],
        body_groups=[["PPE", "earplugs", "mask"], ["gap", "sold_out", "unavailable"], ["backup", "own", "procurement"]],
    )
    return drafted and not has_reservation(env, "mer_7a4c19d2")


CHECKS = [("s10_ppe_discovered", s10_ppe_discovered, 2.0), ("s10_ppe_recovery_draft", s10_ppe_recovery_draft, 1.5)]
