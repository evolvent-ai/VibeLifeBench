from __future__ import annotations
from . import _helpers as H

def s1_official_rules_collected(env) -> bool:
    return H.s1_official_rules_collected(env)

def s1_rule_subscription_or_notice_read(env) -> bool:
    return H.s1_rule_subscription_or_notice_read(env)

CHECKS = [
    ("s1_official_rules_collected", s1_official_rules_collected, 1.5),
    ("s1_rule_subscription_or_notice_read", s1_rule_subscription_or_notice_read, 1.25)
]
