from __future__ import annotations
from ._helpers import *


def s7_qa_reviewed(env) -> bool:
    qa_calls = matching_calls(env, 7, "review_platform", "get_merchant_qa")
    deal_list_calls = matching_calls(env, 7, "review_platform", "list_merchant_deals")
    qa_blob = "\n".join(flat(call.get("result")) for call in qa_calls).lower()
    deal_blob = "\n".join(flat(call.get("result")) for call in deal_list_calls).lower()
    qa_merchants = trace_result_ids(env, 7, "review_platform", "get_merchant_qa", "mer")
    deal_merchants = trace_result_ids(env, 7, "review_platform", "list_merchant_deals", "mer")
    deal_ids = trace_result_ids(env, 7, "review_platform", "get_deal", "deal")
    return (
        len(qa_merchants) >= 2
        and qa_merchants.issubset(deal_merchants)
        and len(deal_ids) >= 3
        and all(term in qa_blob for term in ("invoice", "accessible", "ingredients", "bilingual", "cancellation"))
        and all(term in deal_blob for term in ("33", "invoice", "cancellable"))
    )


CHECKS = [("s7_qa_reviewed", s7_qa_reviewed, 1.25)]
