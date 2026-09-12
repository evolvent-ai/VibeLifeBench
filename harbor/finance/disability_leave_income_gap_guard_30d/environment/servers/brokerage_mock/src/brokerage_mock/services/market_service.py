"""Quote + symbol lookup. Read-only."""
import logging
import sqlite3
from typing import Optional

from ..utils.exceptions import SymbolNotFoundError

logger = logging.getLogger(__name__)


class MarketService:
    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn

    # ------------------------------------------------------------------
    # Helpers used by other services as well
    # ------------------------------------------------------------------
    def latest_quote_row(self, symbol: str) -> Optional[sqlite3.Row]:
        """Return the most recent quote row in ``quotes_daily``, or None.

        v3: no sim clock; the latest row in the table is the latest.
        """
        return self.conn.execute(
            "SELECT * FROM quotes_daily WHERE symbol = ? "
            "ORDER BY date DESC LIMIT 1",
            (symbol,),
        ).fetchone()

    def prev_close_minor(self, symbol: str) -> Optional[int]:
        """Return the close from the row immediately before the latest."""
        rows = self.conn.execute(
            "SELECT close_minor FROM quotes_daily WHERE symbol = ? "
            "ORDER BY date DESC LIMIT 2",
            (symbol,),
        ).fetchall()
        if len(rows) < 2:
            return None
        return int(rows[1]["close_minor"])

    def symbol_name(self, symbol: str) -> str:
        row = self.conn.execute(
            "SELECT name FROM symbols WHERE symbol = ?", (symbol,)
        ).fetchone()
        return row["name"] if row else symbol

    def symbol_kind(self, symbol: str) -> str:
        row = self.conn.execute(
            "SELECT kind FROM symbols WHERE symbol = ?", (symbol,)
        ).fetchone()
        return row["kind"] if row else "stock"

    # ------------------------------------------------------------------
    # Public tool surface
    # ------------------------------------------------------------------
    def get_quote(self, symbol: str) -> dict:
        symbol = (symbol or "").strip()
        if not symbol:
            raise SymbolNotFoundError("symbol is required")
        q = self.latest_quote_row(symbol)
        if not q:
            raise SymbolNotFoundError(f"no quote data for symbol '{symbol}'")
        prev_close = self.prev_close_minor(symbol)
        close = int(q["close_minor"])
        if prev_close is None or prev_close == 0:
            day_change_bp = 0
        else:
            day_change_bp = int(round((close - prev_close) * 10000 / prev_close))
        # bid/ask: emulate 5 bp spread around last
        spread = max(1, close // 2000)
        bid = max(1, close - spread)
        ask = close + spread
        return {
            "symbol": symbol,
            "name": self.symbol_name(symbol),
            "bid_minor": bid,
            "ask_minor": ask,
            "last_minor": close,
            "prev_close_minor": prev_close if prev_close is not None else close,
            "day_change_bp": day_change_bp,
            "as_of_date": q["date"],
        }
