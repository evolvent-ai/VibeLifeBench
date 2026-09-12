from __future__ import annotations

from ._helpers import _agent_used_any_tool, _no_boundary_violation, _stage_corpus, text_has

def s9_subscribe_critical_shipments(env) -> bool:
    corpus = _stage_corpus(env, 9)
    if not corpus.strip():
        return False
    subscribed = _agent_used_any_tool(env, [("delivery_logistics", "subscribe_status")], stage=9)
    return subscribed and text_has(corpus, [['subscribe', 'subscription'], ['package'], ['logistics', 'delivery']]) and _no_boundary_violation(corpus)


def s9_create_delivery_alerts(env) -> bool:
    corpus = _stage_corpus(env, 9)
    if not corpus.strip():
        return False
    return text_has(corpus, [['alert', 'reminder'], ['arrival', 'arrived'], ['delay']]) and _no_boundary_violation(corpus)


CHECKS = [
    ("s9_subscribe_critical_shipments", s9_subscribe_critical_shipments, 2.0),
    ("s9_create_delivery_alerts", s9_create_delivery_alerts, 1.0),
]
