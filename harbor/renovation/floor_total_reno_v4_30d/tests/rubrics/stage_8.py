"""Stage 8 — select a dynamically optimal flooring-repair cart without ordering."""
from .shared import _helpers as R
from .shared import _helpers as H

def s8_table(env):
    return H.repair_catalog(env) and (R.artifact_has(env, "/workspace/gear_plan.md", (
        ("sku",), ("inventory", "stock"), ("coupon", "coupon"),
        ("baseboard",), ("80mm", "80 mm"), ("silver gray", "silver-gray"), ("aluminum alloy",), ("8 m", "8 m", "8 m"),
        ("transition strip", "t-molding"), ("t-shaped", "t-molding"), ("30mm", "30 mm"), ("2.4 m", "2.4 m"), ("4 pieces", "four pieces"),
        ("moisture-barrier underlayment",), ("ixpe",), ("aluminum film", "aluminum-film"), ("2mm", "2 mm"), ("20 square meters", "20 square meters", "20 square meters"),
        ("not ordered", "not_ordered"),
    )))

def s8_optimal(env):
    return R.cart_is_dynamic_optimum(env, "usr_lai_xu", ("bnd_qflr_a", "bnd_qflr_b", "bnd_qflr_c"), as_of="2026-06-22") and R.no_new_order(env, after="2026-06-22T00:00:00+08:00") and R.artifact_active(env, "/workspace/budget.md")

CHECKS = [("s8_table", s8_table, 4.0), ("s8_optimal", s8_optimal, 3.0)]
