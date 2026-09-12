"""Stage 8 — select a dynamically optimal three-item cart without ordering."""
from .shared import _helpers as R
from .shared import _backend as B


def s8_table(env):
    return B.optimized_cart(env) and R.artifact_has(env, "/workspace/gear_plan.md", (
        ("sku",), ("inventory", "stock"), ("coupon",),
        ("hinges",), ("110-degree", "110°"), ("full-overlay",), ("35mm", "35 mm"), ("pack of 10", "10-pack"),
        ("drawer slides",), ("400mm", "400 mm"), ("side-mount",), ("ball-bearing",), ("25kg", "25 kg"),
        ("wood primer", "clear primer"), ("1kg", "1 kg"), ("water-based",), ("clear",),
        ("not ordered", "not_ordered"),
    ))


def s8_optimal(env):
    return B.optimized_cart(env) and R.artifact_active(env, "/workspace/budget.md")


CHECKS = [("s8_table", s8_table, 4.0), ("s8_optimal", s8_optimal, 3.0)]
