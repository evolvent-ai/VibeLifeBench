from __future__ import annotations
from ._helpers import *

def s21_forklift_update(env) -> bool:
    discovered = merchant_qa_has(env, "mer_7a4c19d2", ["叉车通道", "拍照点", "大厅"])
    acted = used_tool(env, 21, "review_platform", "get_merchant_qa") and (used_tool(env, 21, "notion") or used_tool(env, 21, "notification_hub") or used_tool(env, 21, "email"))
    return discovered and acted and durable_has(env, [["叉车"], ["拍照点", "合影点"], ["关闭", "大厅"], ["分组", "顺序"]])

CHECKS = [("s21_forklift_update", s21_forklift_update, 1.5)]
