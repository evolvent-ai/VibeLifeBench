from __future__ import annotations
from ._helpers import *


def s16_approver_reply(env) -> bool:
    return (
        used_tool(env, 16, "email", "save_draft")
        and draft_matches(env, "safety boundaries", "approver", ["route intensity", "dietary", "bilingual", "sensitive information", "pending confirmation"], stage=16)
        and workspace_has(env, "CITY_CULTURE_PLAN.json", ["route intensity", "dietary boundaries", "bilingual reminders", "sensitive information"], 3, stage=16)
    )


CHECKS = [("s16_approver_reply", s16_approver_reply, 1.5)]
