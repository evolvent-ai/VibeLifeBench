"""Account, portfolio, positions, and performance queries (read-only)."""
import logging
import sqlite3
from typing import List, Optional

from ..backends.db import latest_snapshot_date
from ..utils.dates import add_days, ytd_start
from ..utils.exceptions import AccountNotFoundError, BadArgError
from .market_service import MarketService

logger = logging.getLogger(__name__)


class AccountService:
    def __init__(self, conn: sqlite3.Connection, market: MarketService):
        self.conn = conn
        self.market = market

    def list_accounts(self, user_id: str) -> List[dict]:
        rows = self.conn.execute(
            "SELECT account_id, broker, account_type, opened_at, status "
            "FROM accounts WHERE user_id = ? ORDER BY opened_at",
            (user_id,),
        ).fetchall()
        return [dict(r) for r in rows]

    def _require_account(self, account_id: str) -> sqlite3.Row:
        row = self.conn.execute(
            "SELECT * FROM accounts WHERE account_id = ?", (account_id,)
        ).fetchone()
        if not row:
            raise AccountNotFoundError(f"account '{account_id}' not found")
        return row

    def get_portfolio(self, account_id: str) -> dict:
        acct = self._require_account(account_id)
        positions = self._positions_with_prices(account_id)
        positions_value = sum(p["market_value_minor"] for p in positions)
        todays_pnl = 0
        for p in positions:
            prev = self.market.prev_close_minor(p["symbol"])
            if prev is None:
                continue
            qty_milli = p["_qty_milli"]
            todays_pnl += qty_milli * (p["current_price_minor"] - prev) // 1000
        return {
            "account_id": account_id,
            "cash_minor": int(acct["cash_minor"]),
            "positions_value_minor": int(positions_value),
            "total_value_minor": int(acct["cash_minor"]) + int(positions_value),
            "todays_pnl_minor": int(todays_pnl),
            "as_of_date": latest_snapshot_date(self.conn, account_id),
        }

    def get_positions(self, account_id: str) -> List[dict]:
        self._require_account(account_id)
        positions = self._positions_with_prices(account_id)
        out = []
        for p in positions:
            out.append({
                "symbol": p["symbol"],
                "name": p["name"],
                "kind": p["kind"],
                "qty": p["qty"],
                "avg_cost_minor": p["avg_cost_minor"],
                "current_price_minor": p["current_price_minor"],
                "market_value_minor": p["market_value_minor"],
                "unrealized_pnl_minor": p["unrealized_pnl_minor"],
            })
        return out

    def _positions_with_prices(self, account_id: str) -> List[dict]:
        rows = self.conn.execute(
            "SELECT symbol, kind, qty_milli, avg_cost_minor FROM positions "
            "WHERE account_id = ? AND qty_milli > 0 ORDER BY symbol",
            (account_id,),
        ).fetchall()
        out: List[dict] = []
        for r in rows:
            symbol = r["symbol"]
            kind = r["kind"]
            qty_milli = int(r["qty_milli"])
            avg_cost = int(r["avg_cost_minor"])
            price = self._current_price_minor(symbol, kind)
            mv = qty_milli * price // 1000
            cost_basis = qty_milli * avg_cost // 1000
            qty_display: float
            if kind == "stock":
                qty_display = qty_milli // 1000
            else:
                qty_display = round(qty_milli / 1000.0, 3)
            out.append({
                "symbol": symbol,
                "name": self.market.symbol_name(symbol),
                "kind": kind,
                "qty": qty_display,
                "_qty_milli": qty_milli,
                "avg_cost_minor": avg_cost,
                "current_price_minor": price,
                "market_value_minor": mv,
                "unrealized_pnl_minor": mv - cost_basis,
            })
        return out

    def _current_price_minor(self, symbol: str, kind: str) -> int:
        if kind == "fund":
            row = self.conn.execute(
                "SELECT current_nav_minor FROM funds WHERE fund_code = ?",
                (symbol,),
            ).fetchone()
            if row:
                return int(row["current_nav_minor"])
            nav_row = self.conn.execute(
                "SELECT nav_minor FROM fund_navs WHERE fund_code = ? "
                "ORDER BY date DESC LIMIT 1",
                (symbol,),
            ).fetchone()
            return int(nav_row["nav_minor"]) if nav_row else 0
        q = self.market.latest_quote_row(symbol)
        return int(q["close_minor"]) if q else 0

    # ------------------------------------------------------------------
    # Performance
    # ------------------------------------------------------------------
    def get_portfolio_perf(self, account_id: str, period: str) -> dict:
        self._require_account(account_id)
        if period not in ("1d", "7d", "30d", "ytd"):
            raise BadArgError("period must be one of: 1d, 7d, 30d, ytd")
        end_date: Optional[str] = latest_snapshot_date(self.conn, account_id)
        if end_date is None:
            return {
                "period_return_bp": 0,
                "max_drawdown_bp": 0,
                "start_value_minor": 0,
                "end_value_minor": 0,
            }
        if period == "1d":
            start_date = add_days(end_date, -1)
        elif period == "7d":
            start_date = add_days(end_date, -7)
        elif period == "30d":
            start_date = add_days(end_date, -30)
        else:
            start_date = ytd_start(end_date)

        snapshots = self.conn.execute(
            "SELECT date, total_value_minor FROM portfolio_snapshots "
            "WHERE account_id = ? AND date >= ? AND date <= ? "
            "ORDER BY date",
            (account_id, start_date, end_date),
        ).fetchall()
        if not snapshots:
            return {
                "period_return_bp": 0,
                "max_drawdown_bp": 0,
                "start_value_minor": 0,
                "end_value_minor": 0,
            }
        start_val = int(snapshots[0]["total_value_minor"])
        end_val = int(snapshots[-1]["total_value_minor"])
        period_return_bp = 0
        if start_val > 0:
            period_return_bp = int(round((end_val - start_val) * 10000 / start_val))

        peak = start_val
        max_dd_bp = 0
        for s in snapshots:
            v = int(s["total_value_minor"])
            if v > peak:
                peak = v
            if peak > 0:
                dd_bp = int(round((peak - v) * 10000 / peak))
                if dd_bp > max_dd_bp:
                    max_dd_bp = dd_bp
        return {
            "period_return_bp": period_return_bp,
            "max_drawdown_bp": max_dd_bp,
            "start_value_minor": start_val,
            "end_value_minor": end_val,
        }
