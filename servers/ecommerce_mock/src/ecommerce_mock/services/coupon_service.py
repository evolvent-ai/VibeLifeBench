"""Coupon validation + effect calculation.

`apply_coupon` mutates `applied_coupons` and returns the recomputed cart
view. `evaluate` is a pure helper used by both apply_coupon and the
cart view recompute.
"""
import sqlite3
from typing import Iterable, List

from ..utils.dates import now_iso_z, today_utc
from ..utils.exceptions import (
    CouponBelowMinError,
    CouponCategoryMismatchError,
    CouponExpiredError,
    CouponInvalidError,
    CouponNotAppliedError,
)


class CouponService:
    def __init__(self, conn: sqlite3.Connection, cart_service=None):
        self.conn = conn
        # cart_service injected post-construction (cyclic dependency).
        self.cart_service = cart_service

    # ---------------- public ----------------
    def apply_coupon(self, user_id: str, code: str) -> dict:
        code = (code or "").strip()
        if not code:
            raise CouponInvalidError("coupon code is empty")

        coupon = self._load_coupon(code)
        self._validate_dates_and_caps(coupon)

        # ensure user has a cart row so applied_coupons FK is satisfied
        self.conn.execute(
            "INSERT INTO carts (user_id, updated_at) VALUES (?, ?) ON CONFLICT(user_id) DO NOTHING",
            (user_id, now_iso_z()),
        )

        cart_rows = self.conn.execute(
            "SELECT * FROM cart_items WHERE user_id = ?", (user_id,)
        ).fetchall()
        if not cart_rows:
            raise CouponInvalidError("cart is empty; cannot apply coupon")

        effect = self.evaluate(code, cart_rows)
        if effect.get("error"):
            self._raise_effect_error(effect)

        # already applied? upsert is idempotent (PK on (user_id, code))
        existing = self.conn.execute(
            "SELECT 1 FROM applied_coupons WHERE user_id = ? AND code = ?",
            (user_id, code),
        ).fetchone()
        if not existing:
            self.conn.execute(
                "INSERT INTO applied_coupons (user_id, code, applied_at) VALUES (?, ?, ?)",
                (user_id, code, now_iso_z()),
            )
        return self.cart_service.get_cart(user_id)

    def remove_coupon(self, user_id: str, code: str) -> dict:
        row = self.conn.execute(
            "SELECT 1 FROM applied_coupons WHERE user_id = ? AND code = ?",
            (user_id, code),
        ).fetchone()
        if not row:
            raise CouponNotAppliedError(f"coupon {code!r} is not applied")
        self.conn.execute(
            "DELETE FROM applied_coupons WHERE user_id = ? AND code = ?",
            (user_id, code),
        )
        return self.cart_service.get_cart(user_id)

    # ---------------- evaluator (pure) ----------------
    def evaluate(self, code: str, cart_rows: Iterable[sqlite3.Row]) -> dict:
        """Return {discount_minor, kind} on success, or {error, code} on
        failure (so callers can decide whether to raise or silently drop).
        """
        try:
            coupon = self._load_coupon(code)
            self._validate_dates_and_caps(coupon)
        except CouponInvalidError as exc:
            return {"error": exc.message, "code": exc.code}
        except CouponExpiredError as exc:
            return {"error": exc.message, "code": exc.code}

        # category filter
        cart_rows = list(cart_rows)
        if not cart_rows:
            return {"error": "cart is empty", "code": "COUPON_INVALID"}

        restriction = coupon["category_restriction"]
        eligible_subtotal = 0
        for r in cart_rows:
            prod = self.conn.execute(
                "SELECT category FROM products WHERE product_id = ?", (r["product_id"],)
            ).fetchone()
            if not prod:
                continue
            line = int(r["unit_price_minor"]) * int(r["qty"])
            if restriction and prod["category"] != restriction:
                continue
            eligible_subtotal += line

        if restriction and eligible_subtotal == 0:
            return {
                "error": f"no eligible items for category '{restriction}'",
                "code": "COUPON_CATEGORY_MISMATCH",
            }
        if int(coupon["min_spend_minor"]) > eligible_subtotal:
            return {
                "error": (
                    f"order eligible subtotal {eligible_subtotal} < required "
                    f"{int(coupon['min_spend_minor'])}"
                ),
                "code": "COUPON_BELOW_MIN",
            }

        kind = coupon["kind"]
        value = int(coupon["value_bp_or_minor"])
        if kind == "percent_off":
            discount = (eligible_subtotal * value) // 10_000
        elif kind == "flat_off":
            discount = min(value, eligible_subtotal)
        elif kind == "free_shipping":
            # No shipping subtotal yet (set at place_order time), so a
            # free_shipping coupon contributes 0 to cart-view discount;
            # the order pipeline zeroes shipping_minor when applied.
            discount = 0
        else:
            return {"error": f"unknown coupon kind {kind!r}", "code": "COUPON_INVALID"}

        return {"discount_minor": int(discount), "kind": kind}

    # ---------------- internals ----------------
    def _load_coupon(self, code: str) -> sqlite3.Row:
        row = self.conn.execute(
            "SELECT * FROM coupons WHERE code = ?", (code,)
        ).fetchone()
        if not row:
            raise CouponInvalidError(f"coupon {code!r} not found")
        if not int(row["active"]):
            raise CouponInvalidError(f"coupon {code!r} is inactive")
        return row

    def _validate_dates_and_caps(self, coupon: sqlite3.Row) -> None:
        today = today_utc()
        if today < coupon["valid_from"]:
            raise CouponInvalidError(
                f"coupon {coupon['code']!r} not yet active (starts {coupon['valid_from']})"
            )
        if today > coupon["valid_until"]:
            raise CouponExpiredError(
                f"coupon {coupon['code']!r} expired on {coupon['valid_until']}"
            )
        max_uses = int(coupon["max_uses"])
        if max_uses > 0 and int(coupon["used_count"]) >= max_uses:
            raise CouponInvalidError(f"coupon {coupon['code']!r} has reached its max_uses")

    def _raise_effect_error(self, effect: dict) -> None:
        code = effect.get("code")
        msg = effect.get("error", "coupon invalid")
        if code == "COUPON_BELOW_MIN":
            raise CouponBelowMinError(msg)
        if code == "COUPON_CATEGORY_MISMATCH":
            raise CouponCategoryMismatchError(msg)
        if code == "COUPON_EXPIRED":
            raise CouponExpiredError(msg)
        raise CouponInvalidError(msg)
