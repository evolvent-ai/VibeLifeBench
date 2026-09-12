from __future__ import annotations
from ._helpers import *

def r22_buy_gel_only(env) -> bool:
    try:
        text = _order_detail_text(env) + "\n" + _trace_text(env, 12, 12) + "\n" + _agent_reply(env, 12)
        return (
            _stage_trace_all(env, 12, [["ecommerce"], ["place_order"], ["add_to_cart"]])
            and any_has(text, ["prod_knee_gel", "prod_ice_pack", "sku_knee_gel", "sku_ice_pack", "cold-compress gel", "ice pack"])
            and any_has(text, ["place_order", "order_id", "paid", "place order"])
            and not any_has(_order_detail_text(env) + "\n" + _trace_text(env, 12, 12), ["prod_knee_device", "sku_knee_device"])
        )
    except Exception:
        return False

def r23_gel_budget_log(env) -> bool:
    try:
        text = _agent_reply(env, 12) + "\n" + wfile(env, "BUDGET_LEDGER.md") + "\n" + _trace_text(env, 12, 12)
        return (
            _stage_trace_all(env, 12, [["banking"], ["pay_payee"], ["list_transactions"], ["ecommerce"], ["place_order"]])
            and _reconciled_order_groups(env, [["prod_knee_gel", "sku_knee_gel", "prod_ice_pack", "sku_ice_pack"]])
            and any_has(text, ["cold-compress", "ice pack", "gel"])
            and any_has(text, ["budget", "ledger", "deduct", "balance", "remaining"])
            and any_has(text, ["800", "under", "below", "small expense"])
            and _notion_has(env, [["cold-compress", "ice pack", "gel"], ["budget", "ledger", "balance", "remaining"], ["800", "under", "below"]])
        )
    except Exception:
        return False

CHECKS = [
    ("r22_buy_gel_only", r22_buy_gel_only, 5.0),
    ("r23_gel_budget_log", r23_gel_budget_log, 4.0),
]
