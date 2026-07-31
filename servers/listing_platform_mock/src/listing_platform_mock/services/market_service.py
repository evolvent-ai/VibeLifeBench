"""Market transaction statistics lookup (成交均价)."""
import logging
import sqlite3
from typing import List

from ..utils.exceptions import BadArgError, StatsNotFoundError

logger = logging.getLogger(__name__)


class MarketService:
    def __init__(self, conn: sqlite3.Connection) -> None:
        self.conn = conn

    def get_market_stats(self, area_or_community: str) -> List[dict]:
        """Return market stats rows whose ``area`` matches (exact, then LIKE)."""
        if not area_or_community:
            raise BadArgError("area_or_community is required")
        rows = self.conn.execute(
            "SELECT * FROM market_stats WHERE area = ? ORDER BY category ASC, period DESC",
            (area_or_community,),
        ).fetchall()
        if not rows:
            like = f"%{area_or_community}%"
            rows = self.conn.execute(
                "SELECT * FROM market_stats WHERE area LIKE ? ORDER BY area ASC, category ASC, period DESC",
                (like,),
            ).fetchall()
        if not rows:
            raise StatsNotFoundError(
                f"no market stats found for area: {area_or_community}"
            )
        return [
            {
                "stat_id": r["stat_id"],
                "area": r["area"],
                "city": r["city"],
                "category": r["category"],
                "avg_price_minor": int(r["avg_price_minor"]),
                "unit": r["unit"],
                "sample_size": int(r["sample_size"]),
                "period": r["period"],
            }
            for r in rows
        ]
