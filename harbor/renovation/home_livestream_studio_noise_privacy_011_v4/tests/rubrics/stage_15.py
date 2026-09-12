from __future__ import annotations

from ._helpers import (
    _agent_used_any_tool,
    _backend_record_count,
    _no_boundary_violation,
    _stage_corpus,
    _workspace_file_text,
    text_has,
)

def s15_detect_overheat_recall(env) -> bool:
    corpus = _stage_corpus(env, 15)
    if not corpus.strip():
        return False
    return text_has(corpus, [['recall'], ['thermal', 'overheat'], ['notification']]) and _no_boundary_violation(corpus)


def s15_stop_using_recalled_light(env) -> bool:
    corpus = _stage_corpus(env, 15)
    if not corpus.strip():
        return False
    source_reads = _agent_used_any_tool(
        env, [("notification_hub", "list_notifications")], stage=15
    ) and _agent_used_any_tool(env, [("ecommerce", "list_orders")], stage=15)
    recall_count = _backend_record_count(
        env,
        "notification_hub",
        "list_notifications",
        [["notif_light_recall"], ["recall"], ["thermal", "overheat"], ["key light", "prod_0001"]],
        user_id="user_lwq",
        limit=500,
    )
    order_count = _backend_record_count(
        env,
        "ecommerce",
        "list_orders",
        [["key light"], ["paid", "refund_requested", "refunded"]],
        user_id="user_lwq",
        limit=100,
    )
    ledger = _workspace_file_text(env, "purchase_ledger.md")
    return (
        source_reads
        and recall_count == 1
        and order_count >= 1
        and text_has(ledger, [["stop"], ["using", "use"], ["recall"], ["official"], ["setup"]])
        and _no_boundary_violation(corpus)
    )


CHECKS = [
    ("s15_detect_overheat_recall", s15_detect_overheat_recall, 2.0),
    ("s15_stop_using_recalled_light", s15_stop_using_recalled_light, 5.0),
]
