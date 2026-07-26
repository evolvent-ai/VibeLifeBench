from __future__ import annotations
from ._helpers import *

def s20_onsite_adjustment(env) -> bool:
    discovered = notification_has(env, "ntf_013_onsite_health") and notification_has(env, "ntf_013_onsite_lang")
    acted = used_tool(env, 20, "notification_hub") and (used_tool(env, 20, "notion") or used_tool(env, 20, "email"))
    return discovered and acted and durable_has(env, [["身体不适", "休息区"], ["英文", "可阅读", "语言支持"], ["升级", "现场联系人", "协助"]])

CHECKS = [("s20_onsite_adjustment", s20_onsite_adjustment, 1.5)]
