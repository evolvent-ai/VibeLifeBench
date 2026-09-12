from __future__ import annotations
import json
from ._helpers import *

def r11_stock_query(env) -> bool:
    try:
        text = _trace_text(env, 5, 5) + "\n" + _agent_reply(env, 5)
        return (
            _stage_trace_all(env, 5, [["ecommerce"], ["get_product", "search_products"]])
            and _trace_result_has(env, 5, lambda result: all(token in json.dumps(result, ensure_ascii=False).lower() for token in ["prod_math_book_01", "sku_math_book_01"]) and any(token in json.dumps(result, ensure_ascii=False).lower() for token in ['"stock": 0', '"quantity": 0', '"qty": 0']))
            and any_has(text, ["quantity", "0", "out of stock", "stock is 0", "sold out"])
        )
    except Exception:
        return False

def r12_book_replace(env) -> bool:
    try:
        text = _order_detail_text(env) + "\n" + _trace_text(env, 5, 5) + "\n" + wfile(env, "BUDGET_LEDGER.md") + "\n" + _notion_text(env)
        return (
            _stage_trace_all(env, 5, [["ecommerce", "product", "cart", "order"], ["place_order", "add_to_cart"]])
            and any_has(text, ["prod_math_book_alt", "sku_math_book_alt", "alternative", "alternative product"])
            and any_has(text, ["order_id", "paid", "place order", "purchase"])
            and _workspace_file_has(env, "BUDGET_LEDGER.md", [["budget", "ledger"], ["alternative", "out of stock", "final-review papers"]])
            and _notion_has(env, [["alternative", "out of stock", "final-review papers"], ["budget", "ledger", "expense"]])
        )
    except Exception:
        return False

CHECKS = [
    ("r11_stock_query", r11_stock_query, 4.0),
    ("r12_book_replace", r12_book_replace, 3.0),
]
