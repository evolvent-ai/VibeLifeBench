from __future__ import annotations
from ._helpers import *


def r35_stationery_order_and_budget_recorded(env) -> bool:
    try:
        backend = _order_detail_text(env)
        durable = wfile(env, "BUDGET_LEDGER.md") + "\n" + _notion_text(env)
        return (
            _stage_trace_all(env, 17, [["ecommerce"], ["place_order"], ["banking"], ["pay_payee"], ["list_transactions"]])
            and _reconciled_order_groups(env, [["prod_stationery", "sku_stationery"]])
            and count_hits(backend, [["prod_stationery", "sku_stationery", "2b", "stationery"], ["order_id", "paid", "placed"]]) == 2
            and count_hits(durable, [["stationery", "2B", "eraser"], ["budget", "balance", "remaining balance"], ["orders", "order_id", "SKU"]]) == 3
        )
    except Exception:
        return False


CHECKS = [("r35_stationery_order_and_budget_recorded", r35_stationery_order_and_budget_recorded, 1.5)]
