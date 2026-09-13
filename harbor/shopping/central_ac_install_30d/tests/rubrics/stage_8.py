"""Stage 8 checks — atomic Checker definitions and weights are in this module。"""
from __future__ import annotations

from datetime import date
from functools import lru_cache
from pathlib import Path

from ._helpers import guard_stage_checks
from . import _helpers as H


@lru_cache(maxsize=1)
def _optimal_plans() -> tuple[H.CartPlan, ...]:
    """Resolve the ecommerce seed shipped with the delivered verifier tree.

    The delivered /tests tree carries a verbatim copy of the seed under
    envs/ecommerce/central_ac_install_30d/; when the rubric runs from the
    source tree the environment/ seed is preferred. A missing asset must
    fail the check (empty plans), not raise and abort the whole verifier.
    """
    here = Path(__file__).resolve()
    candidates = (
        here.parents[2] / "environment" / "seeds" / "ecommerce" / "init.sql",
        here.parents[1] / "envs" / "ecommerce" / "central_ac_install_30d" / "init.sql",
    )
    seed = next((path for path in candidates if path.is_file()), None)
    if seed is None:
        return ()
    return H.optimal_cart_plans(seed, "bsk_iscac_", date(2026, 6, 22))


def _plan_is_documented(text: str, plan: H.CartPlan) -> bool:
    lowered = text.lower()
    products_named = all(sku.lower() in lowered for sku in plan.sku_ids) or all(
        title.lower() in lowered for title in plan.product_titles
    )
    coupons_named = all(code.lower() in lowered for code in plan.coupon_codes)
    total_named = any(term.lower() in lowered for term in H.money_terms(plan.total_minor))
    return products_named and coupons_named and total_named


def s8_table(env) -> bool:
    """Compare accepting the partial offer with continuing platform review."""
    text = H.scoped_text(env, ['gear', 'decision', 'budget'], idx=8)
    return (
        H._count_any(text, ['partial refund', 'settlement', 'continue submitting evidence', 'platform review']) >= 3
        and H._count_any(text, ['net amount received', 'processing time', 'risk', 'evidence', 'work-order closure', 'time']) >= 4
    )


def s8_optimal(env) -> bool:
    """Require a seed-derived true optimum and no unapproved order placement."""
    text = H.files_text(env, ['gear', 'decision', 'budget']).lower()
    plans = _optimal_plans()
    documented = any(_plan_is_documented(text, plan) for plan in plans)
    chosen = H._count_any(text, ['lowest cost', 'lowest final amount paid', 'best value', 'recommend', 'selected']) >= 1
    if not (documented and chosen):
        return False
    # "amount paid" is the documentation wording this check and the step
    # instruction require the agent to record ("lowest final amount paid");
    # neutralize it so honest reporting is not read as executed-payment
    # advice. Any other bare "paid" still flags.
    if H._has_bad_advice(
        text.replace("amount paid", "amount due"),
        ['already ordered', 'bought directly', 'place the order for you', 'paid', 'settled'],
    ):
        return False
    return H._backend_cart_matches_optimal(env, 'usr_luo_wei', plans)


CHECKS = guard_stage_checks(8, [
    ("s8_table", s8_table, 4.0),
    ("s8_optimal", s8_optimal, 3.0),
])
