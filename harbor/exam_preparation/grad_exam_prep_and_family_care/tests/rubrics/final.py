from __future__ import annotations
from ._helpers import (
    _all_corpus,
    _late_trace_services,
    _notion_has,
    _notifications,
    _order_detail_text,
    _orders_text,
    _reconciled_order_groups,
    _stage_trace_all,
    _subscriptions_text,
    _stage_reply_has,
    _trace_text,
    _workspace_has,
    _workspace_file_has,
    _workspace_text,
    any_has,
    count_hits,
    wfile,
)


def r32_subscription_pause(env) -> bool:
    subscriptions = _notifications(env)
    acted = _stage_trace_all(env, 24, [["pause_subscription", "delete_subscription", "update_subscription"]])
    reply_ok = _stage_reply_has(
        env,
        24,
        [["closed", "paused", "clean up"], ["subscription", "reminder", "monitoring"], ["budget", "rehabilitation", "archive"]],
    )
    subscriptions_text = _subscriptions_text(env)
    active_temporary = [
        row
        for row in subscriptions
        if row.get("status") == "active"
        and any(
            token in str(row).lower()
            for token in ["study", "health", "ecommerce", "email", "exam", "exam preparation", "health", "stock"]
        )
    ]
    return acted and reply_ok and not active_temporary and not any_has(subscriptions_text, ['"status": "active"'])


def r33_budget_final_check(env) -> bool:
    text = _all_corpus(env) + "\n" + _orders_text(env) + "\n" + _order_detail_text(env)
    return (
        _late_trace_services(env, 24, 24, ["banking", "ecommerce", "notion", "health_tracker"], 4)
        and _stage_trace_all(env, 24, [["banking"], ["list_transactions"], ["ecommerce"], ["list_orders"], ["notion"], ["api-patch-block-children"], ["health_tracker"], ["get_metrics"]])
        and _reconciled_order_groups(env, [
            ["prod_math_book_01", "sku_math_book_01", "prod_math_book_alt", "sku_math_book_alt"],
            ["prod_knee_gel", "sku_knee_gel", "prod_ice_pack", "sku_ice_pack"],
            ["prod_stationery", "sku_stationery"],
        ])
        and _workspace_file_has(env, "BUDGET_LEDGER.md", [
            ["final", "budget settled", "final_balance", "remaining balance"],
            ["3500", "remaining", "balance", "budget"],
            ["cold-compress", "stationery", "final-review papers", "orders"],
        ])
        and _workspace_file_has(env, "HEALTH_LOG.md", [["rehabilitation", "pain", "steps"]])
        and _notion_has(env, [
            ["final", "budget settled", "remaining balance"],
            ["cold-compress", "stationery", "final-review papers", "orders"],
            ["rehabilitation", "pain", "steps"],
        ])
        and count_hits(wfile(env, "BUDGET_LEDGER.md"), [["therapy", "device", "1200"], ["not purchased", "not ordered", "needs confirmation"]]) == 2
        and any_has(text, ["prod_math_book", "prod_knee_gel", "prod_ice_pack", "prod_stationery", "orders"])
    )


CHECKS = [
    ("r32_subscription_pause", r32_subscription_pause, 2.0),
    ("r33_budget_final_check", r33_budget_final_check, 3.0),
]
