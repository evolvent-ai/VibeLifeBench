"""Address book + order lifecycle (place / list / get / track / cancel)."""
import sqlite3
from typing import List, Optional

from ..backends.db import next_counter
from ..utils.dates import now_iso_z, today_utc
from ..utils.exceptions import (
    AddressNotFoundError,
    BadArgError,
    CartEmptyError,
    OrderNotCancelableError,
    OrderNotFoundError,
    OutOfStockError,
)
from ..utils.ids import address_id, order_id, order_item_id, tracking_no


VALID_ORDER_STATUSES = {
    "pending_payment", "paid", "shipped", "delivered",
    "completed", "refund_requested", "refunded", "cancelled",
}


class OrderService:
    def __init__(
        self,
        conn: sqlite3.Connection,
        cart_service,
        coupon_service,
    ):
        self.conn = conn
        self.cart_service = cart_service
        self.coupon_service = coupon_service

    # ---------------- addresses ----------------
    def list_addresses(self, user_id: str) -> List[dict]:
        rows = self.conn.execute(
            "SELECT * FROM addresses WHERE user_id = ? ORDER BY is_default DESC, address_id",
            (user_id,),
        ).fetchall()
        return [self._address_row_to_dict(r) for r in rows]

    def add_address(
        self,
        user_id: str,
        recipient: str,
        phone: str,
        province: str,
        city: str,
        district: str,
        detail: str,
        postal_code: str,
        is_default: bool = False,
    ) -> dict:
        for field, val in [
            ("recipient", recipient), ("phone", phone), ("province", province),
            ("city", city), ("district", district), ("detail", detail),
            ("postal_code", postal_code),
        ]:
            if not val or not str(val).strip():
                raise BadArgError(f"address field {field!r} is required")

        seq = next_counter(self.conn, "address_seq")
        addr_id = address_id(seq)
        if is_default:
            self.conn.execute(
                "UPDATE addresses SET is_default = 0 WHERE user_id = ?", (user_id,)
            )
        self.conn.execute(
            """
            INSERT INTO addresses
              (address_id, user_id, recipient, phone, province, city, district, detail, postal_code, is_default)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                addr_id, user_id, recipient, phone, province, city,
                district, detail, postal_code, 1 if is_default else 0,
            ),
        )
        row = self.conn.execute(
            "SELECT * FROM addresses WHERE address_id = ?", (addr_id,)
        ).fetchone()
        return self._address_row_to_dict(row)

    def _address_row_to_dict(self, row: sqlite3.Row) -> dict:
        return {
            "address_id": row["address_id"],
            "user_id": row["user_id"],
            "recipient": row["recipient"],
            "phone": row["phone"],
            "province": row["province"],
            "city": row["city"],
            "district": row["district"],
            "detail": row["detail"],
            "postal_code": row["postal_code"],
            "is_default": bool(int(row["is_default"])),
        }

    # ---------------- place order ----------------
    def place_order(
        self,
        user_id: str,
        address_id_: str,
        payment_method: str,
        note: Optional[str] = None,
    ) -> dict:
        if not payment_method or not payment_method.strip():
            raise BadArgError("payment_method is required")

        addr = self.conn.execute(
            "SELECT * FROM addresses WHERE address_id = ? AND user_id = ?",
            (address_id_, user_id),
        ).fetchone()
        if not addr:
            raise AddressNotFoundError(f"address {address_id_!r} not found for user")

        cart_rows = self.conn.execute(
            "SELECT * FROM cart_items WHERE user_id = ? ORDER BY added_at, cart_item_id",
            (user_id,),
        ).fetchall()
        if not cart_rows:
            raise CartEmptyError("cannot place order with empty cart")

        # Stock check before committing anything.
        for r in cart_rows:
            stock = self.conn.execute(
                "SELECT COALESCE(quantity, 0) AS quantity FROM stocks WHERE sku_id = ?",
                (r["sku_id"],),
            ).fetchone()
            on_hand = int(stock["quantity"]) if stock else 0
            if on_hand < int(r["qty"]):
                raise OutOfStockError(
                    f"sku {r['sku_id']!r} only has {on_hand} in stock (cart wants {int(r['qty'])})"
                )

        # Pull recomputed cart view to get authoritative subtotal/discount.
        cart_view = self.cart_service.get_cart(user_id)
        subtotal = int(cart_view["subtotal_minor"])
        discount = int(cart_view["discount_minor"])

        # Shipping: free if any applied coupon kind is free_shipping, else 800 (¥8).
        applied = cart_view.get("applied_coupons") or []
        has_free_ship = any(c.get("kind") == "free_shipping" for c in applied)
        shipping = 0 if has_free_ship else 800
        total = max(0, subtotal - discount) + shipping

        sim_date = today_utc()
        seq = next_counter(self.conn, "order_seq")
        oid = order_id(sim_date, seq)
        now = now_iso_z()
        track = tracking_no(oid)

        self.conn.execute("BEGIN IMMEDIATE;")
        try:
            self.conn.execute(
                """
                INSERT INTO orders (
                  order_id, user_id, address_id, payment_method,
                  subtotal_minor, discount_minor, shipping_minor, total_minor,
                  status, placed_at, note, tracking_no
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'pending_payment', ?, ?, ?)
                """,
                (
                    oid, user_id, address_id_, payment_method,
                    subtotal, discount, shipping, total,
                    now, note, track,
                ),
            )
            self.conn.execute(
                "INSERT INTO order_status_history (order_id, status, set_at) VALUES (?, 'pending_payment', ?)",
                (oid, now),
            )

            # In this mock, "place_order" implicitly authorises payment so
            # the order lands in 'paid' and inventory is committed. This
            # matches the agent-facing contract (status `paid` returned).
            self.conn.execute(
                "UPDATE orders SET status = 'paid' WHERE order_id = ?", (oid,)
            )
            self.conn.execute(
                "INSERT INTO order_status_history (order_id, status, set_at) VALUES (?, 'paid', ?)",
                (oid, now),
            )

            item_count = 0
            for idx, r in enumerate(cart_rows, start=1):
                line_total = int(r["unit_price_minor"]) * int(r["qty"])
                self.conn.execute(
                    """
                    INSERT INTO order_items
                      (item_id, order_id, product_id, sku_id, qty, unit_price_minor, line_total_minor)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        order_item_id(oid, idx),
                        oid,
                        r["product_id"],
                        r["sku_id"],
                        int(r["qty"]),
                        int(r["unit_price_minor"]),
                        line_total,
                    ),
                )
                self.conn.execute(
                    "UPDATE stocks SET quantity = quantity - ? WHERE sku_id = ?",
                    (int(r["qty"]), r["sku_id"]),
                )
                self.conn.execute(
                    "UPDATE products SET sales_count = sales_count + ? WHERE product_id = ?",
                    (int(r["qty"]), r["product_id"]),
                )
                item_count += int(r["qty"])

            # bump coupon used_count and detach
            for c in applied:
                self.conn.execute(
                    "UPDATE coupons SET used_count = used_count + 1 WHERE code = ?", (c["code"],)
                )
            self.conn.execute("DELETE FROM applied_coupons WHERE user_id = ?", (user_id,))
            self.conn.execute("DELETE FROM cart_items WHERE user_id = ?", (user_id,))
            self.conn.execute(
                "UPDATE carts SET updated_at = ? WHERE user_id = ?", (now, user_id)
            )
            self.conn.execute("COMMIT;")
        except Exception:
            self.conn.execute("ROLLBACK;")
            raise

        return {
            "order_id": oid,
            "total_minor": total,
            "item_count": item_count,
            "status": "paid",
        }

    # ---------------- list / get / track ----------------
    def list_orders(
        self, user_id: str, status_filter: Optional[str] = None, limit: int = 20,
    ) -> List[dict]:
        try:
            limit = int(limit)
        except Exception:
            raise BadArgError("limit must be an integer")
        limit = max(1, min(limit, 100))

        params: list = [user_id]
        where_extra = ""
        if status_filter:
            if status_filter not in VALID_ORDER_STATUSES:
                raise BadArgError(f"invalid status_filter '{status_filter}'")
            where_extra = " AND status = ?"
            params.append(status_filter)
        params.append(limit)

        rows = self.conn.execute(
            f"SELECT * FROM orders WHERE user_id = ?{where_extra} ORDER BY placed_at DESC LIMIT ?",
            params,
        ).fetchall()
        return [self._order_header_to_dict(r) for r in rows]

    def get_order(self, order_id_: str) -> dict:
        row = self.conn.execute(
            "SELECT * FROM orders WHERE order_id = ?", (order_id_,)
        ).fetchone()
        if not row:
            raise OrderNotFoundError(f"order {order_id_!r} not found")

        items = self.conn.execute(
            "SELECT * FROM order_items WHERE order_id = ? ORDER BY item_id", (order_id_,)
        ).fetchall()
        history = self.conn.execute(
            "SELECT status, set_at FROM order_status_history WHERE order_id = ? ORDER BY id",
            (order_id_,),
        ).fetchall()
        refunds = self.conn.execute(
            "SELECT * FROM refunds WHERE order_id = ? ORDER BY opened_at", (order_id_,)
        ).fetchall()

        return {
            **self._order_header_to_dict(row),
            "items": [
                {
                    "item_id": i["item_id"],
                    "product_id": i["product_id"],
                    "sku_id": i["sku_id"],
                    "qty": int(i["qty"]),
                    "unit_price_minor": int(i["unit_price_minor"]),
                    "line_total_minor": int(i["line_total_minor"]),
                }
                for i in items
            ],
            "status_history": [
                {"status": h["status"], "set_at": h["set_at"]} for h in history
            ],
            "refunds": [
                {
                    "refund_id": rf["refund_id"],
                    "item_id": rf["item_id"],
                    "qty": int(rf["qty"]),
                    "status": rf["status"],
                    "refund_amount_minor": int(rf["refund_amount_minor"]),
                }
                for rf in refunds
            ],
        }

    def _order_header_to_dict(self, row: sqlite3.Row) -> dict:
        return {
            "order_id": row["order_id"],
            "user_id": row["user_id"],
            "address_id": row["address_id"],
            "payment_method": row["payment_method"],
            "subtotal_minor": int(row["subtotal_minor"]),
            "discount_minor": int(row["discount_minor"]),
            "shipping_minor": int(row["shipping_minor"]),
            "total_minor": int(row["total_minor"]),
            "status": row["status"],
            "placed_at": row["placed_at"],
            "note": row["note"],
            "tracking_no": row["tracking_no"],
        }

    def cancel_order(self, order_id_: str, reason: str) -> dict:
        if not reason or not reason.strip():
            raise BadArgError("reason is required")
        row = self.conn.execute(
            "SELECT * FROM orders WHERE order_id = ?", (order_id_,)
        ).fetchone()
        if not row:
            raise OrderNotFoundError(f"order {order_id_!r} not found")
        if row["status"] not in ("pending_payment", "paid"):
            raise OrderNotCancelableError(
                f"order in status {row['status']!r} cannot be cancelled"
            )

        now = now_iso_z()
        self.conn.execute("BEGIN IMMEDIATE;")
        try:
            self.conn.execute(
                "UPDATE orders SET status = 'cancelled' WHERE order_id = ?", (order_id_,)
            )
            self.conn.execute(
                "INSERT INTO order_status_history (order_id, status, set_at) VALUES (?, 'cancelled', ?)",
                (order_id_, now),
            )
            # release stock that had been committed at place_order time
            if row["status"] == "paid":
                for it in self.conn.execute(
                    "SELECT sku_id, qty FROM order_items WHERE order_id = ?", (order_id_,)
                ).fetchall():
                    self.conn.execute(
                        "UPDATE stocks SET quantity = quantity + ? WHERE sku_id = ?",
                        (int(it["qty"]), it["sku_id"]),
                    )
            self.conn.execute("COMMIT;")
        except Exception:
            self.conn.execute("ROLLBACK;")
            raise

        return {
            "order_id": order_id_,
            "status": "cancelled",
            "reason": reason,
            "cancelled_at": now,
        }

    def track_order(self, order_id_: str) -> dict:
        row = self.conn.execute(
            "SELECT order_id, status, tracking_no FROM orders WHERE order_id = ?",
            (order_id_,),
        ).fetchone()
        if not row:
            raise OrderNotFoundError(f"order {order_id_!r} not found")
        latest = self.conn.execute(
            "SELECT status, set_at FROM order_status_history "
            "WHERE order_id = ? ORDER BY id DESC LIMIT 1",
            (order_id_,),
        ).fetchone()
        return {
            "order_id": row["order_id"],
            "tracking_no": row["tracking_no"],
            "latest_status": latest["status"] if latest else row["status"],
            "updated_at": latest["set_at"] if latest else None,
        }
