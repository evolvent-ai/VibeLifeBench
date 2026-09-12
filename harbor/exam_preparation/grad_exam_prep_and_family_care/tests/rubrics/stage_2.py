from __future__ import annotations
from ._helpers import *

def r07_initial_purchase(env) -> bool:
    try:
        text = _order_detail_text(env) + "\n" + _trace_text(env, 2, 2)
        return (
            _stage_trace_all(env, 2, [["ecommerce"], ["place_order"], ["add_to_cart"]])
            and count_hits(text, [
                ["prod_math_book_01", "sku_math_book_01", "final-review papers"],
                ["prod_ice_pack", "sku_ice_pack", "ice pack"],
                ["prod_stationery", "sku_stationery", "stationery", "error", "notebook"],
            ]) >= 2
            and any_has(text, ["place_order", "order_id", "paid"])
            and not any_has(text, ["prod_knee_device", "premium", "therapy", "device"])
        )
    except Exception:
        return False

def r08_budget_log(env) -> bool:
    try:
        corpus = wfile(env, "BUDGET_LEDGER.md") + "\n" + _notion_text(env)
        return (
            _stage_trace_all(env, 2, [["banking"], ["pay_payee"], ["list_transactions"], ["ecommerce"], ["place_order"]])
            and _reconciled_order_groups(env, [["prod_math_book_01", "sku_math_book_01"], ["prod_ice_pack", "sku_ice_pack"], ["prod_stationery", "sku_stationery"]])
            and count_hits(corpus, [["budget", "BUDGET", "ledger"], ["3500"], ["800"], ["balance", "remaining", "deduct", "expense"]]) == 4
            and any_has(corpus, ["ordersday", "order_id", "prod_math_book", "prod_ice_pack", "prod_stationery"])
        )
    except Exception:
        return False

CHECKS = [
    ("r07_initial_purchase", r07_initial_purchase, 2.0),
    ("r08_budget_log", r08_budget_log, 3.0),
]
