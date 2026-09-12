from __future__ import annotations
from ._helpers import *


def s11_photo_rule_recorded(env) -> bool:
    drafted = used_tool(env, 11, "email", "save_draft") and draft_has(
        env,
        subject_groups=[["no-photography", "photography"]],
        recipient_terms=["security"],
        body_groups=[["customer prototype", "customer"], ["no-photography"], ["lobby", "photo"], ["group photo"]],
    )
    return used_tool(env, 11, "email", "search_emails") and drafted


CHECKS = [("s11_photo_rule_recorded", s11_photo_rule_recorded, 1.5)]
