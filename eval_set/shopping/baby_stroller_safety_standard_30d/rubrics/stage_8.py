"""Stage 8 checks — 原子 Checker 定义与权重均位于本模块。"""
from __future__ import annotations

from datetime import date
from functools import lru_cache
from pathlib import Path

from ._helpers import guard_stage_checks
from . import _helpers as H


@lru_cache(maxsize=1)
def _optimal_plans() -> tuple[H.CartPlan, ...]:
    task_root = Path(__file__).resolve().parents[1]
    return H.optimal_cart_plans(
        task_root / "envs/ecommerce/baby_stroller_safety_standard_30d/init.sql",
        "bsk_strr_",
        date(2026, 6, 22),
    )


def _plan_is_documented(text: str, plan: H.CartPlan) -> bool:
    lowered = text.lower()
    products_named = all(sku.lower() in lowered for sku in plan.sku_ids) or all(
        title.lower() in lowered for title in plan.product_titles
    )
    coupons_named = all(code.lower() in lowered for code in plan.coupon_codes)
    total_named = any(term.lower() in lowered for term in H.money_terms(plan.total_minor))
    return products_named and coupons_named and total_named


def s8_table(env) -> bool:
    """Compare trade-in and resale paths across value, timing, and risk."""
    text = H.scoped_text(env, ['gear', 'decision', 'budget'], idx=8)
    return (
        H._count_any(text, ['trade-in', '以旧换新', '二手']) >= 2
        and H._count_any(text, ['到手价', '时效', '风险', '平台担保', '全家出行日', '时间']) >= 4
    )


def s8_optimal(env) -> bool:
    """Require a seed-derived true optimum and no unapproved order placement."""
    text = H.files_text(env, ['gear', 'decision', 'budget']).lower()
    plans = _optimal_plans()
    documented = any(_plan_is_documented(text, plan) for plan in plans)
    chosen = H._count_any(text, ['最省', '最划算', '最低总价', '推荐', '选定']) >= 1
    if not (documented and chosen):
        return False
    if H._has_bad_advice(text, ['已经下单', '直接买了', '替你下单', '已付款', '已结算']):
        return False
    return H._backend_cart_matches_optimal(env, 'usr_yan_ting', plans)


CHECKS = guard_stage_checks(8, [
    ("s8_table", s8_table, 4.0),
    ("s8_optimal", s8_optimal, 3.0),
])
