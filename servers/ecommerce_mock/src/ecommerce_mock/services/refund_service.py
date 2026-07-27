"""Refund submission. Approval happens via orchestrator-issued mutations."""
import sqlite3

from ..backends.db import next_counter
from ..utils.dates import days_between, now_iso_z, today_utc
from ..utils.exceptions import (
    BadArgError,
    OrderItemNotFoundError,
    OrderNotFoundError,
    RefundWindowClosedError,
)
from ..utils.ids import refund_id


REFUND_WINDOW_DAYS = 7
REFUND_ELIGIBLE_STATUSES = {"paid", "shipped", "delivered", "completed", "refund_requested"}


class RefundService:
    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn

    def request_refund(
        self,
        order_id_: str,
        item_id: str,
        qty: int,
        reason: str,
    ) -> dict:
        try:
            qty = int(qty)
        except Exception:
            raise BadArgError("qty must be an integer")
        if qty <= 0:
            raise BadArgError("qty must be positive")
        if not reason or not reason.strip():
            raise BadArgError("reason is required")

        order = self.conn.execute(
            "SELECT order_id, status, placed_at FROM orders WHERE order_id = ?",
            (order_id_,),
        ).fetchone()
        if not order:
            raise OrderNotFoundError(f"order {order_id_!r} not found")
        if order["status"] not in REFUND_ELIGIBLE_STATUSES:
            raise RefundWindowClosedError(
                f"order in status {order['status']!r} is not refund-eligible"
            )

        item = self.conn.execute(
            "SELECT * FROM order_items WHERE item_id = ? AND order_id = ?",
            (item_id, order_id_),
        ).fetchone()
        if not item:
            raise OrderItemNotFoundError(
                f"item {item_id!r} not found on order {order_id_!r}"
            )
        if qty > int(item["qty"]):
            raise BadArgError(
                f"refund qty {qty} exceeds purchased qty {int(item['qty'])}"
            )

        # 7-day return window relative to wall-clock UTC date
        today = today_utc()
        placed_date = order["placed_at"][:10]
        try:
            if days_between(placed_date, today) > REFUND_WINDOW_DAYS:
                raise RefundWindowClosedError(
                    f"refund window closed (>{REFUND_WINDOW_DAYS} days since order)"
                )
        except ValueError:
            # placed_at may be a UTC iso (e.g. with time component) — accept best-effort
            pass

        amount = int(item["unit_price_minor"]) * qty

        seq = next_counter(self.conn, "refund_seq")
        rid = refund_id(today, seq)
        now = now_iso_z()
        self.conn.execute("BEGIN IMMEDIATE;")
        try:
            self.conn.execute(
                """
                INSERT INTO refunds (
                  refund_id, order_id, item_id, qty, reason, status,
                  opened_at, refund_amount_minor
                ) VALUES (?, ?, ?, ?, ?, 'submitted', ?, ?)
                """,
                (rid, order_id_, item_id, qty, reason, now, amount),
            )
            # transition the parent order to refund_requested only if not
            # already past that point.
            if order["status"] in ("paid", "shipped", "delivered", "completed"):
                self.conn.execute(
                    "UPDATE orders SET status = 'refund_requested' WHERE order_id = ?",
                    (order_id_,),
                )
                self.conn.execute(
                    "INSERT INTO order_status_history (order_id, status, set_at) "
                    "VALUES (?, 'refund_requested', ?)",
                    (order_id_, now),
                )
            self.conn.execute("COMMIT;")
        except Exception:
            self.conn.execute("ROLLBACK;")
            raise

        return {
            "refund_id": rid,
            "order_id": order_id_,
            "item_id": item_id,
            "qty": qty,
            "status": "submitted",
            "refund_amount_minor": amount,
            "opened_at": now,
        }
