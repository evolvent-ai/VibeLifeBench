"""Fund catalog browsing, NAV history, subscribe / redeem."""
import logging
import sqlite3
from typing import List, Optional

from ..backends.db import next_counter
from ..utils.exceptions import (
    AccountNotFoundError,
    FundNotFoundError,
    InsufficientCashError,
    InsufficientSharesError,
    InvalidAmountError,
)
from ..utils.ids import now_iso_z, order_id as make_order_id

logger = logging.getLogger(__name__)

ALLOWED_CATEGORIES = {"money_market", "bond", "equity", "mixed", "index"}


class FundService:
    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn

    # ------------------------------------------------------------------
    # Catalog
    # ------------------------------------------------------------------
    def list_funds(self, category: Optional[str] = None) -> List[dict]:
        if category is not None and category not in ALLOWED_CATEGORIES:
            raise InvalidAmountError(
                f"category must be one of {sorted(ALLOWED_CATEGORIES)} or null"
            )
        if category:
            rows = self.conn.execute(
                "SELECT fund_code, fund_name, category, current_nav_minor, "
                "ytd_return_bp, risk_level FROM funds WHERE category = ? "
                "ORDER BY fund_code",
                (category,),
            ).fetchall()
        else:
            rows = self.conn.execute(
                "SELECT fund_code, fund_name, category, current_nav_minor, "
                "ytd_return_bp, risk_level FROM funds ORDER BY fund_code"
            ).fetchall()
        return [
            {
                "fund_code": r["fund_code"],
                "fund_name": r["fund_name"],
                "category": r["category"],
                "nav_minor": int(r["current_nav_minor"]),
                "ytd_return_bp": int(r["ytd_return_bp"]),
                "risk_level": int(r["risk_level"]),
            }
            for r in rows
        ]

    def get_fund_nav(self, fund_code: str, lookback_days: int = 30) -> List[dict]:
        self._require_fund(fund_code)
        lookback_days = max(1, min(int(lookback_days or 30), 365))
        # v3: no sim clock; return the most recent ``lookback_days`` rows
        # ordered most-recent-first.
        rows = self.conn.execute(
            "SELECT date, nav_minor FROM fund_navs WHERE fund_code = ? "
            "ORDER BY date DESC LIMIT ?",
            (fund_code, lookback_days),
        ).fetchall()
        return [{"date": r["date"], "nav_minor": int(r["nav_minor"])} for r in rows]

    # ------------------------------------------------------------------
    # subscribe / redeem
    # ------------------------------------------------------------------
    def subscribe_fund(
        self,
        account_id: str,
        fund_code: str,
        amount_minor: int,
    ) -> dict:
        acct = self._require_account(account_id)
        fund = self._require_fund(fund_code)
        if not isinstance(amount_minor, int) or amount_minor <= 0:
            raise InvalidAmountError("amount_minor must be a positive integer")
        if int(acct["cash_minor"]) < amount_minor:
            raise InsufficientCashError(
                f"need {amount_minor} minor, have {int(acct['cash_minor'])}"
            )
        nav = int(fund["current_nav_minor"])
        if nav <= 0:
            raise InvalidAmountError(f"fund '{fund_code}' has no NAV")
        # units_milli = amount_minor / nav * 1000, rounded down to 2 decimal
        # places (i.e. multiples of 10 milli).
        units_milli_exact = amount_minor * 1000 // nav
        units_milli = (units_milli_exact // 10) * 10
        if units_milli <= 0:
            raise InvalidAmountError(
                "amount too small to acquire any fractional units (min 0.01 units)"
            )
        actual_cost = units_milli * nav // 1000

        self.conn.execute(
            "UPDATE accounts SET cash_minor = cash_minor - ? WHERE account_id = ?",
            (actual_cost, account_id),
        )
        self._credit_fund_position(account_id, fund_code, units_milli, nav)

        seq = next_counter(self.conn, "order_seq")
        oid = make_order_id(seq)
        now = now_iso_z()
        self.conn.execute(
            """
            INSERT INTO orders (
              order_id, account_id, symbol, side, qty_milli,
              order_type, limit_price_minor, tif, status,
              placed_at, filled_at, fill_price_minor
            ) VALUES (?, ?, ?, 'buy', ?, 'market', NULL, 'day', 'filled', ?, ?, ?)
            """,
            (oid, account_id, fund_code, units_milli, now, now, nav),
        )
        return {
            "order_id": oid,
            "status": "filled",
            "units_acquired_milli": int(units_milli),
        }

    def redeem_fund(
        self,
        account_id: str,
        fund_code: str,
        units_milli: int,
    ) -> dict:
        self._require_account(account_id)
        fund = self._require_fund(fund_code)
        if not isinstance(units_milli, int) or units_milli <= 0:
            raise InvalidAmountError("units_milli must be a positive integer")
        pos = self.conn.execute(
            "SELECT qty_milli FROM positions WHERE account_id = ? AND symbol = ?",
            (account_id, fund_code),
        ).fetchone()
        held = int(pos["qty_milli"]) if pos else 0
        if held < units_milli:
            raise InsufficientSharesError(
                f"hold {held} milli-units, attempting to redeem {units_milli}"
            )
        nav = int(fund["current_nav_minor"])
        proceeds = units_milli * nav // 1000

        self.conn.execute(
            "UPDATE accounts SET cash_minor = cash_minor + ? WHERE account_id = ?",
            (proceeds, account_id),
        )
        self.conn.execute(
            "UPDATE positions SET qty_milli = qty_milli - ? "
            "WHERE account_id = ? AND symbol = ?",
            (units_milli, account_id, fund_code),
        )

        seq = next_counter(self.conn, "order_seq")
        oid = make_order_id(seq)
        now = now_iso_z()
        self.conn.execute(
            """
            INSERT INTO orders (
              order_id, account_id, symbol, side, qty_milli,
              order_type, limit_price_minor, tif, status,
              placed_at, filled_at, fill_price_minor
            ) VALUES (?, ?, ?, 'sell', ?, 'market', NULL, 'day', 'filled', ?, ?, ?)
            """,
            (oid, account_id, fund_code, units_milli, now, now, nav),
        )
        return {
            "order_id": oid,
            "status": "filled",
            "units_redeemed_milli": int(units_milli),
            "proceeds_minor": int(proceeds),
        }

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------
    def _require_account(self, account_id: str) -> sqlite3.Row:
        row = self.conn.execute(
            "SELECT * FROM accounts WHERE account_id = ?", (account_id,)
        ).fetchone()
        if not row:
            raise AccountNotFoundError(f"account '{account_id}' not found")
        return row

    def _require_fund(self, fund_code: str) -> sqlite3.Row:
        row = self.conn.execute(
            "SELECT * FROM funds WHERE fund_code = ?", (fund_code,)
        ).fetchone()
        if not row:
            raise FundNotFoundError(f"fund '{fund_code}' not found")
        return row

    def _credit_fund_position(
        self,
        account_id: str,
        fund_code: str,
        units_milli: int,
        nav_minor: int,
    ) -> None:
        existing = self.conn.execute(
            "SELECT qty_milli, avg_cost_minor FROM positions "
            "WHERE account_id = ? AND symbol = ?",
            (account_id, fund_code),
        ).fetchone()
        if existing:
            old_qty = int(existing["qty_milli"])
            old_avg = int(existing["avg_cost_minor"])
            new_qty = old_qty + units_milli
            new_avg = (old_qty * old_avg + units_milli * nav_minor) // new_qty
            self.conn.execute(
                "UPDATE positions SET qty_milli = ?, avg_cost_minor = ? "
                "WHERE account_id = ? AND symbol = ?",
                (new_qty, new_avg, account_id, fund_code),
            )
        else:
            self.conn.execute(
                "INSERT INTO positions (account_id, symbol, kind, qty_milli, avg_cost_minor) "
                "VALUES (?, ?, 'fund', ?, ?)",
                (account_id, fund_code, units_milli, nav_minor),
            )
