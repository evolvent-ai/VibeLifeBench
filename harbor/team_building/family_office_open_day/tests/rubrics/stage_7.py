from __future__ import annotations
from ._helpers import *

def s7_signup_notice_draft_only(env) -> bool:
    notice_action = used(env, 7, "notification_hub", "create") or used(env, 7, "email", "save") or used(env, 7, "notion", "API")
    return notice_action and stage_persisted(env, 7, [["registration"], ["necessary", "restrictions"], ["draft", "reminder"], ["unsent", "pending"]])

CHECKS = [
    ('s7_signup_notice_draft_only', s7_signup_notice_draft_only, 1.25),
]
