"""Stage 8 — select a dynamically optimal drainage-repair cart without ordering."""
from __future__ import annotations

import itertools
import json
import math
import re
from typing import Any

from .shared import _helpers as R

AS_OF = "2026-06-22"
USER_ID = "usr_yong_wei"
COUPON_RULES = (
    ("PAISHUI30", "flat_off", 3000, 26000),
    ("PUZHUANG70", "flat_off", 7000, 29800),
    ("YUSHUI120", "flat_off", 12000, 54000),
    ("TINGYUAN12", "percent_off", 1200, 10000),
)
SPECS = (
    {"material": "304_stainless", "channel_width_mm": 100, "angle_deg": 90, "corner": "inner"},
    {"material": "304_stainless", "size_mm": "300x300", "type": "recessed", "load_class": "C250"},
    {"material": "pervious_concrete", "weight_kg": 25, "color": "dark_gray", "setting": "rapid"},
)


def _candidate_groups(env: Any) -> list[list[dict[str, Any]]]:
    rows: list[tuple[Any, ...]] = []
    for detail in R.trace_results(env, 8, "ecommerce", "get_product"):
        if not isinstance(detail, dict):
            continue
        product_id = detail.get("product_id")
        category = detail.get("category", "")
        for sku in detail.get("skus") or []:
            if isinstance(sku, dict):
                attrs = sku.get("attrs") if isinstance(sku.get("attrs"), dict) else {}
                rows.append((product_id, category, sku.get("sku_id"), json.dumps(attrs, ensure_ascii=False), sku.get("price_minor"), sku.get("stock", 0)))
    groups: list[list[dict[str, Any]]] = []
    for spec in SPECS:
        matches: list[dict[str, Any]] = []
        for product_id, category, sku_id, attrs_raw, price, quantity in rows:
            try:
                attrs = json.loads(str(attrs_raw))
            except (TypeError, json.JSONDecodeError):
                continue
            if all(attrs.get(key) == value for key, value in spec.items()):
                matches.append({
                    "product_id": str(product_id),
                    "category": str(category),
                    "sku_id": str(sku_id),
                    "price": int(price),
                    "quantity": int(quantity),
                })
        groups.append(matches)
    return groups


def _eligible_coupons(env: Any) -> list[list[Any]]:
    # Coupon rows are not part of the immutable catalog snapshot. These are the
    # four authoritative catalog rules, while stage-8 trace/results prove the
    # agent actually inspected and applied the offers it selected.
    return [[code, kind, value, minimum, "2026-06-01", "2026-08-31", None, 0, 0, 1] for code, kind, value, minimum in COUPON_RULES]


def _coupon_discount(coupon: list[Any], items: tuple[dict[str, Any], ...]) -> int | None:
    _code, kind, value, minimum, _start, _end, restriction, _cap, _used, _active = coupon
    eligible = sum(item["price"] for item in items if not restriction or item["category"] == restriction)
    if (restriction and eligible == 0) or eligible < int(minimum):
        return None
    if kind == "percent_off":
        return eligible * int(value) // 10_000
    if kind == "flat_off":
        return min(int(value), eligible)
    if kind == "free_shipping":
        return 0
    return None


def _best_selections(env: Any) -> tuple[list[list[dict[str, Any]]], list[list[Any]], set[tuple[tuple[str, ...], tuple[str, ...]]], int | None]:
    groups = _candidate_groups(env)
    coupons = _eligible_coupons(env)
    if len(groups) != len(SPECS) or any(not group for group in groups):
        return groups, coupons, set(), None
    best_total = math.inf
    best: set[tuple[tuple[str, ...], tuple[str, ...]]] = set()
    for combo in itertools.product(*groups):
        subtotal = sum(item["price"] for item in combo)
        for mask in range(1 << len(coupons)):
            codes: list[str] = []
            discount = 0
            valid = True
            for index, coupon in enumerate(coupons):
                if not mask & (1 << index):
                    continue
                effect = _coupon_discount(coupon, combo)
                if effect is None:
                    valid = False
                    break
                codes.append(str(coupon[0]))
                discount += effect
            if not valid:
                continue
            total = max(0, subtotal - discount)
            key = (tuple(sorted(item["sku_id"] for item in combo)), tuple(sorted(codes)))
            if total < best_total:
                best_total = total
                best = {key}
            elif total == best_total:
                best.add(key)
    return groups, coupons, best, None if math.isinf(best_total) else int(best_total)


def s8_table(env):
    groups, coupons, best, best_total = _best_selections(env)
    if not best or best_total is None:
        return False
    text_ok = R.artifact_has(env, "/workspace/gear_plan.md", (
        ("sku",), ("inventory", "stock"), ("coupon",),
        ("drainage-channel corner", "drainage channel"), ("304",), ("100mm", "100 mm"), ("90°", "90 degrees"), ("inner corner",),
        ("manhole cover",), ("recessed",), ("300×300", "300x300"), ("c250",),
        ("permeable concrete",), ("rapid-setting",), ("dark gray",), ("25kg", "25 kg"),
        ("not ordered", "not_ordered"),
    ))
    if not text_ok:
        return False
    text = R.read_text(env, "/workspace/gear_plan.md").lower()
    candidate_skus = {item["sku_id"].lower() for group in groups for item in group}
    coupon_codes = {str(row[0]).lower() for row in coupons}

    def amount_written(minor: int) -> bool:
        cents = re.search(rf"(?<!\d){minor}(?!\d)", text)
        yuan = re.search(rf"(?<!\d){minor / 100:.2f}(?!\d)", text)
        return bool(cents or yuan)

    thresholds_written = all(amount_written(int(row[3])) for row in coupons)
    return (
        all(sku in text for sku in candidate_skus)
        and all(code in text for code in coupon_codes)
        and thresholds_written
        and amount_written(best_total)
    )


def s8_optimal(env):
    groups, _coupons, best, _best_total = _best_selections(env)
    if not best:
        return False
    carts = [row for row in R.trace_results(env, 8, "ecommerce", "get_cart") if isinstance(row, dict)]
    if not carts:
        return False
    cart = carts[-1]
    cart_rows = [[row.get("product_id"), row.get("sku_id"), row.get("qty"), row.get("unit_price_minor")] for row in cart.get("items") or [] if isinstance(row, dict)]
    if len(cart_rows) != len(groups) or any(int(row[2]) != 1 for row in cart_rows):
        return False
    current_prices = {
        item["sku_id"]: (item["product_id"], item["price"])
        for group in groups for item in group
    }
    if any(
        str(row[1]) not in current_prices
        or str(row[0]) != current_prices[str(row[1])][0]
        or int(row[3]) != current_prices[str(row[1])][1]
        for row in cart_rows
    ):
        return False
    selected = tuple(sorted(str(row[1]) for row in cart_rows))
    codes = tuple(sorted(str(row.get("code")) for row in cart.get("applied_coupons") or [] if isinstance(row, dict) and row.get("code")))
    return (
        (selected, codes) in best
        and R.no_new_order(env, after="2026-06-22T00:00:00+08:00")
        and R.artifact_active(env, "/workspace/budget.md")
    )


CHECKS = [("s8_table", s8_table, 4.0), ("s8_optimal", s8_optimal, 3.0)]
