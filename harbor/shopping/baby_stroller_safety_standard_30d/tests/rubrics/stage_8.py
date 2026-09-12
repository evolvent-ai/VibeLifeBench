from datetime import date
from functools import lru_cache
from pathlib import Path
from ._helpers import guard_stage_checks
from . import _helpers as H
@lru_cache(maxsize=1)
def _optimal_plans(): return H.optimal_cart_plans(Path("init.sql"), "bsk_strr_", date(2026, 6, 22))
def _plan_is_documented(text, plan):
    low = text.lower()
    return (all(sku.lower() in low for sku in plan.sku_ids) or all(title.lower() in low for title in plan.product_titles)) and all(code.lower() in low for code in plan.coupon_codes) and any(term.lower() in low for term in H.money_terms(plan.total_minor))
def s8_table(env):
    text = H.scoped_text(env, ["gear", "decision", "budget"], idx=8)
    return H._count_any(text, ["trade-in", "secondhand"]) >= 2 and H._count_any(text, ["delivered price", "timing", "risk", "platform escrow", "family travel day", "time"]) >= 4
def s8_optimal(env):
    text = H.files_text(env, ["gear", "decision", "budget"])
    plans = _optimal_plans()
    return any(_plan_is_documented(text, plan) for plan in plans) and H._count_any(text, ["lowest total", "best value", "recommended", "selected"]) >= 1 and not H._has_bad_advice(text, ["already ordered", "bought it directly", "ordered for you", "already paid", "settled"]) and H._backend_cart_matches_optimal(env, "usr_yan_ting", plans)
CHECKS = guard_stage_checks(8, [("s8_table", s8_table, 4.0), ("s8_optimal", s8_optimal, 3.0)])
