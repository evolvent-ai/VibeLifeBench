from __future__ import annotations
from ._helpers import *

def s20_onsite_adjustment(env) -> bool:
    discovered = notification_has(env, "ntf_013_onsite_health") and notification_has(env, "ntf_013_onsite_lang")
    acted = used_tool(env, 20, "notification_hub") and (used_tool(env, 20, "notion") or used_tool(env, 20, "email"))
    return discovered and acted and durable_has(env, [["unwell", "rest area", "rest", "area"], ["English", "readable", "language support", "language"], ["onsite", "contact"]])

CHECKS = [("s20_onsite_adjustment", s20_onsite_adjustment, 1.5)]
