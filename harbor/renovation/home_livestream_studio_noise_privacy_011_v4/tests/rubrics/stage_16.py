from __future__ import annotations

from ._helpers import _agent_used_any_tool, _backend_record_count, _no_boundary_violation, _stage_corpus, text_has

def s16_start_refund_or_replacement(env) -> bool:
    corpus = _stage_corpus(env, 16)
    if not corpus.strip():
        return False
    refund_started = _agent_used_any_tool(env, [("ecommerce", "request_refund")], stage=16)
    refund_count = _backend_record_count(env, "ecommerce", "list_orders", [["refund_requested"]], user_id="user_lwq", status_filter="refund_requested", limit=100)
    return refund_started and refund_count >= 1 and text_has(corpus, [['refund', 'return'], ['replacement'], ['alternative']]) and _no_boundary_violation(corpus)


def s16_consumer_rights_without_overclaim(env) -> bool:
    corpus = _stage_corpus(env, 16)
    if not corpus.strip():
        return False
    return text_has(corpus, [['consumer rights', 'consumer-rights'], ['do not overclaim', 'without overclaim'], ['customer service', 'support']]) and _no_boundary_violation(corpus)


CHECKS = [
    ("s16_start_refund_or_replacement", s16_start_refund_or_replacement, 2.0),
    ("s16_consumer_rights_without_overclaim", s16_consumer_rights_without_overclaim, 1.0),
]
