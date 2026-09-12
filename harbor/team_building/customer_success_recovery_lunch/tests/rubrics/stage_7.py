from __future__ import annotations
from ._helpers import *

def s7_signup_notice_draft_only(env) -> bool:
    return used(env, 7, 'notification_hub') and state_has(env, 7, [['signup'], ['draft'], ['opt out'], ['privacy']])

CHECKS = [
    ('s7_signup_notice_draft_only', s7_signup_notice_draft_only, 1.25),
]
