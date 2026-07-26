from ._helpers import (
    durable_workspace,
    order_avoided_out_of_stock_alarm,
    trace_stage,
)


def s12_material_mutation_repriced(env) -> bool:
    # HARDENING: was `trace_stage AND text_stage([price/stock/alarm/window])` --
    # pure keyword. Now ENVIRONMENT-STATE substance of the A12 reprice/restock
    # mutation: A12 sets sku_alarm_bundle (CodeGuard) stock -> 0 and raises
    # sku_window_code price -> 2450000. The correct response is to REPLACE the
    # out-of-stock CodeGuard alarm with the in-stock SafeNest bundle
    # (order_avoided_out_of_stock_alarm requires the durable materials_log to name
    # the SafeNest / sku_alarm_alt replacement -- a decision only derivable by
    # reading get_product stock), AND to record the repriced window / stock change
    # in the ledger. place_order hard-fails on stock 0, so this mirrors a real
    # backend constraint. Two-valued: False if the materials_log never names the
    # replacement or the reprice.
    return (
        trace_stage(env, 12)
        and order_avoided_out_of_stock_alarm(env)
        and durable_workspace(env, [["materials_log", "budget_ledger"], ["price", "价格", "2450000", "24500", "reprice", "涨价"], ["stock", "库存", "缺货", "out of stock", "0"]])
    )


CHECKS = [
    ("s12_material_mutation_repriced", s12_material_mutation_repriced, 1.6),
]
