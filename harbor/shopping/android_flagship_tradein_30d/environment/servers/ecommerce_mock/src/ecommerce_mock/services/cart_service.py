"""Cart operations: read, add, update, remove. Pricing of the cart
(including coupon-driven discount and total) is centralised in
`_compute_cart_view` so `add/update/remove/apply_coupon/remove_coupon`
all return the same shape.
"""
import sqlite3
from typing import List, Optional

from ..backends.db import next_counter
from ..utils.dates import now_iso_z
from ..utils.exceptions import (
    BadArgError,
    CartItemNotFoundError,
    OutOfStockError,
    ProductNotFoundError,
    SkuNotFoundError,
)
from ..utils.ids import cart_item_id


class CartService:
    def __init__(self, conn: sqlite3.Connection, coupon_service=None):
        self.conn = conn
        self.coupon_service = coupon_service  # injected after construction; see server.py

    # ---------------- public ----------------
    def get_cart(self, user_id: str) -> dict:
        self._ensure_cart_row(user_id)
        return self._compute_cart_view(user_id)

    def add_to_cart(self, user_id: str, product_id: str, sku_id: str, qty: int) -> dict:
        try:
            qty = int(qty)
        except Exception:
            raise BadArgError("qty must be an integer")
        if qty <= 0:
            raise BadArgError("qty must be positive")

        sku = self.conn.execute(
            "SELECT s.sku_id, s.product_id, s.price_minor, COALESCE(st.quantity, 0) AS quantity "
            "FROM skus s LEFT JOIN stocks st ON st.sku_id = s.sku_id WHERE s.sku_id = ?",
            (sku_id,),
        ).fetchone()
        if not sku:
            raise SkuNotFoundError(f"sku {sku_id!r} not found")
        if sku["product_id"] != product_id:
            raise ProductNotFoundError(f"sku {sku_id!r} does not belong to product {product_id!r}")
        if int(sku["quantity"]) < qty:
            raise OutOfStockError(
                f"sku {sku_id!r} only has {int(sku['quantity'])} in stock"
            )

        self._ensure_cart_row(user_id)
        # If the (user, sku) line already exists, increment qty.
        existing = self.conn.execute(
            "SELECT cart_item_id, qty FROM cart_items WHERE user_id = ? AND sku_id = ?",
            (user_id, sku_id),
        ).fetchone()
        now = now_iso_z()
        if existing:
            new_qty = int(existing["qty"]) + qty
            if int(sku["quantity"]) < new_qty:
                raise OutOfStockError(
                    f"sku {sku_id!r} only has {int(sku['quantity'])} in stock"
                )
            self.conn.execute(
                "UPDATE cart_items SET qty = ?, unit_price_minor = ? WHERE cart_item_id = ?",
                (new_qty, int(sku["price_minor"]), existing["cart_item_id"]),
            )
        else:
            seq = next_counter(self.conn, "cart_item_seq")
            ci_id = cart_item_id(seq)
            self.conn.execute(
                """
                INSERT INTO cart_items
                  (cart_item_id, user_id, product_id, sku_id, qty, unit_price_minor, added_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (ci_id, user_id, product_id, sku_id, qty, int(sku["price_minor"]), now),
            )
        self.conn.execute(
            "UPDATE carts SET updated_at = ? WHERE user_id = ?", (now, user_id)
        )
        return self._compute_cart_view(user_id)

    def update_cart_item(self, user_id: str, cart_item_id_: str, qty: int) -> dict:
        try:
            qty = int(qty)
        except Exception:
            raise BadArgError("qty must be an integer")
        if qty < 0:
            raise BadArgError("qty must be >= 0")

        row = self.conn.execute(
            "SELECT * FROM cart_items WHERE cart_item_id = ? AND user_id = ?",
            (cart_item_id_, user_id),
        ).fetchone()
        if not row:
            raise CartItemNotFoundError(f"cart item {cart_item_id_!r} not found for user")

        if qty == 0:
            self.conn.execute(
                "DELETE FROM cart_items WHERE cart_item_id = ?", (cart_item_id_,)
            )
        else:
            stock = self.conn.execute(
                "SELECT COALESCE(quantity, 0) AS quantity FROM stocks WHERE sku_id = ?",
                (row["sku_id"],),
            ).fetchone()
            on_hand = int(stock["quantity"]) if stock else 0
            if on_hand < qty:
                raise OutOfStockError(f"sku {row['sku_id']!r} only has {on_hand} in stock")
            self.conn.execute(
                "UPDATE cart_items SET qty = ? WHERE cart_item_id = ?", (qty, cart_item_id_)
            )
        self.conn.execute(
            "UPDATE carts SET updated_at = ? WHERE user_id = ?", (now_iso_z(), user_id)
        )
        return self._compute_cart_view(user_id)

    def remove_from_cart(self, user_id: str, cart_item_id_: str) -> dict:
        row = self.conn.execute(
            "SELECT cart_item_id FROM cart_items WHERE cart_item_id = ? AND user_id = ?",
            (cart_item_id_, user_id),
        ).fetchone()
        if not row:
            raise CartItemNotFoundError(f"cart item {cart_item_id_!r} not found for user")
        self.conn.execute("DELETE FROM cart_items WHERE cart_item_id = ?", (cart_item_id_,))
        self.conn.execute(
            "UPDATE carts SET updated_at = ? WHERE user_id = ?", (now_iso_z(), user_id)
        )
        return self._compute_cart_view(user_id)

    # ---------------- internal helpers ----------------
    def _ensure_cart_row(self, user_id: str) -> None:
        self.conn.execute(
            "INSERT INTO carts (user_id, updated_at) VALUES (?, ?) "
            "ON CONFLICT(user_id) DO NOTHING",
            (user_id, now_iso_z()),
        )

    def _load_cart_items(self, user_id: str) -> List[sqlite3.Row]:
        return self.conn.execute(
            "SELECT * FROM cart_items WHERE user_id = ? ORDER BY added_at, cart_item_id",
            (user_id,),
        ).fetchall()

    def _load_applied_codes(self, user_id: str) -> List[str]:
        rows = self.conn.execute(
            "SELECT code FROM applied_coupons WHERE user_id = ? ORDER BY applied_at",
            (user_id,),
        ).fetchall()
        return [r["code"] for r in rows]

    def _compute_cart_view(self, user_id: str) -> dict:
        rows = self._load_cart_items(user_id)
        items = []
        subtotal = 0
        for r in rows:
            unit = int(r["unit_price_minor"])
            qty = int(r["qty"])
            line = unit * qty
            subtotal += line
            items.append({
                "cart_item_id": r["cart_item_id"],
                "product_id": r["product_id"],
                "sku_id": r["sku_id"],
                "qty": qty,
                "unit_price_minor": unit,
                "line_total_minor": line,
            })

        applied_codes = self._load_applied_codes(user_id)
        discount = 0
        applied_details: List[dict] = []
        if self.coupon_service and applied_codes:
            # Pricing pass; auto-detach coupons that no longer qualify.
            still_valid: List[str] = []
            for code in applied_codes:
                effect = self.coupon_service.evaluate(code, rows)
                if effect.get("error"):
                    self.conn.execute(
                        "DELETE FROM applied_coupons WHERE user_id = ? AND code = ?",
                        (user_id, code),
                    )
                    continue
                discount += int(effect["discount_minor"])
                applied_details.append({
                    "code": code,
                    "kind": effect["kind"],
                    "discount_minor": int(effect["discount_minor"]),
                })
                still_valid.append(code)

        total = max(0, subtotal - discount)
        return {
            "user_id": user_id,
            "items": items,
            "subtotal_minor": subtotal,
            "applied_coupons": applied_details,
            "discount_minor": discount,
            "total_minor": total,
        }
