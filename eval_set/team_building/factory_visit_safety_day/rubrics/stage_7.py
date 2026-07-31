from __future__ import annotations
from ._helpers import *

def s7_qa_reviewed(env) -> bool:
    calls = used_tool_with_value(env, 7, "review_platform", "get_merchant_qa", ["mer_7a4c19d2"]) and used_tool_with_value(env, 7, "review_platform", "list_merchant_deals", ["mer_7a4c19d2"]) and used_tool_with_value(env, 7, "review_platform", "get_deal", ["deal_factory_013_visit"]) and used_tool_with_value(env, 7, "review_platform", "get_deal", ["deal_factory_013_ppe"])
    backend = merchant_qa_has(env, "mer_7a4c19d2", ["发票", "禁拍", "押金"]) and merchant_detail_has(env, "mer_7a4c19d2", ["嘉兴", "参访"])
    return calls and backend and durable_has(env, [["发票"], ["禁拍"], ["ppe", "耳塞", "口罩"], ["退", "取消"]])

CHECKS = [("s7_qa_reviewed", s7_qa_reviewed, 1.5)]
