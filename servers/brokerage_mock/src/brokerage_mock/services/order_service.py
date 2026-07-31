"""Order placement, listing, and cancellation."""
import logging
import sqlite3
from typing import List, Optional

from ..backends.db import next_counter
from ..utils.exceptions import (
    AccountNotFoundError,
    BadArgError,
    BadOrderTypeError,
    BadSideError,
    InsufficientCashError,
    InsufficientSharesError,
    OrderNotFoundError,
    OrderNotPendingError,
    SymbolNotFoundError,
)
from ..utils.ids import now_iso_z, order_id as make_order_id
from .market_service import MarketService

logger = logging.getLogger(__name__)

ALLOWED_SIDES = {"buy", "sell"}
ALLOWED_ORDER_TYPES = {"market", "limit"}
ALLOWED_STATUS_FILTERS = {"pending", "filled", "cancelled", "rejected"}


class OrderService:
    def __init__(self, conn: sqlite3.Connection, market: MarketService):
        self.conn = conn
        self.market = market

    # ------------------------------------------------------------------
    # list_orders
    # ------------------------------------------------------------------
    def list_orders(
        self,
        account_id: str,
        status_filter: Optional[str] = None,
        limit: int = 50,
    ) -> List[dict]:
        self._require_account(account_id)
        if status_filter and status_filter not in ALLOWED_STATUS_FILTERS:
            raise BadArgError(
                f"status_filter must be one of {sorted(ALLOWED_STATUS_FILTERS)}"
            )
        limit = max(1, min(int(limit or 50), 500))
        if status_filter:
            rows = self.conn.execute(
                "SELECT * FROM orders WHERE account_id = ? AND status = ? "
                "ORDER BY placed_at DESC LIMIT ?",
                (account_id, status_filter, limit),
            ).fetchall()
        else:
            rows = self.conn.execute(
                "SELECT * FROM orders WHERE account_id = ? "
                "ORDER BY placed_at DESC LIMIT ?",
                (account_id, limit),
            ).fetchall()
        return [self._order_row_to_dict(r) for r in rows]

    # ------------------------------------------------------------------
    # place_order
    # ------------------------------------------------------------------
    def place_order(
        self,
        account_id: str,
        symbol: str,
        side: str,
        qty: int,
        order_type: str,
        limit_price_minor: Optional[int] = None,
        tif: str = "day",
    ) -> dict:
        acct = self._require_account(account_id)
        if side not in ALLOWED_SIDES:
            raise BadSideError("side must be 'buy' or 'sell'")
        if order_type not in ALLOWED_ORDER_TYPES:
            raise BadOrderTypeError("order_type must be 'market' or 'limit'")
        if not isinstance(qty, int) or qty <= 0:
            raise BadArgError("qty must be a positive integer (whole shares)")
        if order_type == "limit":
            if not isinstance(limit_price_minor, int) or limit_price_minor <= 0:
                raise BadArgError(
                    "limit_price_minor (positive int) is required for limit orders"
                )

        q = self.market.latest_quote_row(symbol)
        if not q:
            raise SymbolNotFoundError(f"no quote data for symbol '{symbol}'")
        last_price = int(q["close_minor"])

        qty_milli = qty * 1000  # stocks are stored as whole-share milli-units

        # Validate funds / holdings for market orders that fill immediately.
        # For limit orders we still pre-check so the agent gets a fast error
        # rather than a deferred pending that will never fill cleanly.
        ref_price = last_price if order_type == "market" else int(limit_price_minor)
        if side == "buy":
            required_cash = qty_milli * ref_price // 1000
            if int(acct["cash_minor"]) < required_cash:
                raise InsufficientCashError(
                    f"need {required_cash} minor, have {int(acct['cash_minor'])}"
                )
        else:  # sell
            pos = self.conn.execute(
                "SELECT qty_milli FROM positions WHERE account_id = ? AND symbol = ?",
                (account_id, symbol),
            ).fetchone()
            held_milli = int(pos["qty_milli"]) if pos else 0
            if held_milli < qty_milli:
                raise InsufficientSharesError(
                    f"hold {held_milli // 1000} shares, attempting to sell {qty}"
                )

        seq = next_counter(self.conn, "order_seq")
        oid = make_order_id(seq)
        placed_at = now_iso_z()

        if order_type == "market":
            self._insert_order_filled(
                oid, account_id, symbol, side, qty_milli,
                "market", None, tif, placed_at, last_price,
            )
            self._apply_fill(account_id, symbol, side, qty_milli, last_price)
            return {
                "order_id": oid,
                "status": "filled",
                "fill_price_minor": last_price,
            }

        # Limit order: see if it would cross immediately at today's price.
        crosses = (
            (side == "buy" and last_price <= int(limit_price_minor))
            or (side == "sell" and last_price >= int(limit_price_minor))
        )
        if crosses:
            fill_price = last_price
            self._insert_order_filled(
                oid, account_id, symbol, side, qty_milli,
                "limit", int(limit_price_minor), tif, placed_at, fill_price,
            )
            self._apply_fill(account_id, symbol, side, qty_milli, fill_price)
            return {
                "order_id": oid,
                "status": "filled",
                "fill_price_minor": fill_price,
            }

        # Otherwise queue as pending; admin advance day may fill it.
        self.conn.execute(
            """
            INSERT INTO orders (
              order_id, account_id, symbol, side, qty_milli,
              order_type, limit_price_minor, tif, status, placed_at
            ) VALUES (?, ?, ?, ?, ?, 'limit', ?, ?, 'pending', ?)
            """,
            (oid, account_id, symbol, side, qty_milli,
             int(limit_price_minor), tif, placed_at),
        )
        return {"order_id": oid, "status": "pending"}

    # ------------------------------------------------------------------
    # cancel_order
    # ------------------------------------------------------------------
    def cancel_order(self, order_id: str) -> dict:
        row = self.conn.execute(
            "SELECT * FROM orders WHERE order_id = ?", (order_id,)
        ).fetchone()
        if not row:
            raise OrderNotFoundError(f"order '{order_id}' not found")
        if row["status"] != "pending":
            raise OrderNotPendingError(
                f"order '{order_id}' is in status '{row['status']}', not pending"
            )
        self.conn.execute(
            "UPDATE orders SET status = 'cancelled', filled_at = NULL WHERE order_id = ?",
            (order_id,),
        )
        return {"order_id": order_id, "status": "cancelled"}

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------
    def _require_account(self, account_id: str) -> sqlite3.Row:
        row = self.conn.execute(
            "SELECT * FROM accounts WHERE account_id = ?", (account_id,)
        ).fetchone()
        if not row:
            raise AccountNotFoundError(f"account '{account_id}' not found")
        return row

    def _insert_order_filled(
        self,
        oid: str,
        account_id: str,
        symbol: str,
        side: str,
        qty_milli: int,
        order_type: str,
        limit_price_minor: Optional[int],
        tif: str,
        placed_at: str,
        fill_price: int,
    ) -> None:
        self.conn.execute(
            """
            INSERT INTO orders (
              order_id, account_id, symbol, side, qty_milli,
              order_type, limit_price_minor, tif, status,
              placed_at, filled_at, fill_price_minor
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'filled', ?, ?, ?)
            """,
            (oid, account_id, symbol, side, qty_milli,
             order_type, limit_price_minor, tif,
             placed_at, placed_at, fill_price),
        )

    def _apply_fill(
        self,
        account_id: str,
        symbol: str,
        side: str,
        qty_milli: int,
        price_minor: int,
    ) -> None:
        """Mutate cash + position rows for a fill at `price_minor`."""
        cost = qty_milli * price_minor // 1000
        if side == "buy":
            self.conn.execute(
                "UPDATE accounts SET cash_minor = cash_minor - ? WHERE account_id = ?",
                (cost, account_id),
            )
            self._credit_position(account_id, symbol, qty_milli, price_minor)
        else:
            self.conn.execute(
                "UPDATE accounts SET cash_minor = cash_minor + ? WHERE account_id = ?",
                (cost, account_id),
            )
            self._debit_position(account_id, symbol, qty_milli)

    def _credit_position(
        self,
        account_id: str,
        symbol: str,
        qty_milli: int,
        price_minor: int,
    ) -> None:
        existing = self.conn.execute(
            "SELECT qty_milli, avg_cost_minor FROM positions "
            "WHERE account_id = ? AND symbol = ?",
            (account_id, symbol),
        ).fetchone()
        if existing:
            old_qty = int(existing["qty_milli"])
            old_avg = int(existing["avg_cost_minor"])
            new_qty = old_qty + qty_milli
            # Volume-weighted average cost in minor units (avg_cost is per-share).
            new_avg = (old_qty * old_avg + qty_milli * price_minor) // new_qty
            self.conn.execute(
                "UPDATE positions SET qty_milli = ?, avg_cost_minor = ? "
                "WHERE account_id = ? AND symbol = ?",
                (new_qty, new_avg, account_id, symbol),
            )
        else:
            kind = self.market.symbol_kind(symbol)
            self.conn.execute(
                "INSERT INTO positions (account_id, symbol, kind, qty_milli, avg_cost_minor) "
                "VALUES (?, ?, ?, ?, ?)",
                (account_id, symbol, kind, qty_milli, price_minor),
            )

    def _debit_position(self, account_id: str, symbol: str, qty_milli: int) -> None:
        self.conn.execute(
            "UPDATE positions SET qty_milli = qty_milli - ? "
            "WHERE account_id = ? AND symbol = ?",
            (qty_milli, account_id, symbol),
        )
        # leave the row in place even at 0 qty so avg_cost history is preserved;
        # _positions_with_prices filters qty_milli > 0.

    def _order_row_to_dict(self, r: sqlite3.Row) -> dict:
        qty_milli = int(r["qty_milli"])
        kind = self.market.symbol_kind(r["symbol"])
        if kind == "stock":
            qty: float = qty_milli // 1000
        else:
            qty = round(qty_milli / 1000.0, 3)
        return {
            "order_id": r["order_id"],
            "symbol": r["symbol"],
            "side": r["side"],
            "qty": qty,
            "order_type": r["order_type"],
            "limit_price_minor": (
                int(r["limit_price_minor"]) if r["limit_price_minor"] is not None else None
            ),
            "status": r["status"],
            "placed_at": r["placed_at"],
            "filled_at": r["filled_at"],
            "fill_price_minor": (
                int(r["fill_price_minor"]) if r["fill_price_minor"] is not None else None
            ),
        }
