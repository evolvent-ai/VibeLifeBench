from __future__ import annotations
from ._helpers import *

def s21_forklift_update(env) -> bool:
    discovered = merchant_qa_has(env, "mer_7a4c19d2", ["forklift lane", "photo point", "lobby"])
    acted = used_tool(env, 21, "review_platform", "get_merchant_qa") and (used_tool(env, 21, "notion") or used_tool(env, 21, "notification_hub") or used_tool(env, 21, "email"))
    return discovered and acted and durable_has(env, [["forklift"], ["photo point", "group-photo point"], ["close", "lobby"], ["group", "order"]])

CHECKS = [("s21_forklift_update", s21_forklift_update, 1.5)]
