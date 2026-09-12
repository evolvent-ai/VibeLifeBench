"""Merchant discovery: search, detail, recommendations."""
import logging
import sqlite3
from typing import List, Optional

from ..utils.exceptions import BadArgError, BadCategoryError
from ._common import fetch_merchant, merchant_detail, merchant_summary

logger = logging.getLogger(__name__)

VALID_SORTS = ("rating", "price_asc", "price_desc", "review_count")

def _distinct(conn, table: str, col: str) -> set:
    """Values present in a corpus column; defined by the task's seed."""
    return {r[0] for r in conn.execute(f"SELECT DISTINCT {col} FROM {table}")}



class MerchantService:
    def __init__(self, conn: sqlite3.Connection) -> None:
        self.conn = conn

    def search_merchants(
        self,
        category: str,
        city: Optional[str] = None,
        area: Optional[str] = None,
        min_rating: Optional[float] = None,
        price_band: Optional[str] = None,
        sort: str = "rating",
        limit: int = 20,
        page: int = 1,
    ) -> dict:
        cats = _distinct(self.conn, "merchants", "category")
        if cats and category not in cats:
            raise BadCategoryError(
                "category must be one of " + ", ".join(sorted(cats)))
        if price_band is not None:
            bands = _distinct(self.conn, "merchants", "price_band")
            if bands and price_band not in bands:
                raise BadArgError(
                    "price_band must be one of " + ", ".join(sorted(bands)))
        if sort not in VALID_SORTS:
            raise BadArgError(f"sort must be one of {VALID_SORTS}")
        if limit is None or limit < 1:
            raise BadArgError("limit must be >= 1")
        if limit > 100:
            limit = 100
        if page is None or page < 1:
            raise BadArgError("page must be >= 1")

        where = ["category = ?"]
        args: List = [category]
        if city:
            where.append("city = ?")
            args.append(city)
        if area:
            where.append("area = ?")
            args.append(area)
        if price_band:
            where.append("price_band = ?")
            args.append(price_band)
        if min_rating is not None:
            where.append("rating_tenths >= ?")
            args.append(int(round(float(min_rating) * 10)))

        order = {
            "rating": "rating_tenths DESC, review_count DESC",
            "price_asc": "avg_price_minor ASC",
            "price_desc": "avg_price_minor DESC",
            "review_count": "review_count DESC",
        }[sort]

        where_sql = " AND ".join(where)
        total = int(self.conn.execute(
            f"SELECT COUNT(*) AS n FROM merchants WHERE {where_sql}", args
        ).fetchone()["n"])
        offset = (page - 1) * int(limit)
        rows = self.conn.execute(
            f"SELECT * FROM merchants WHERE {where_sql} ORDER BY {order}, merchant_id ASC LIMIT ? OFFSET ?",
            args + [int(limit), offset],
        ).fetchall()
        return {
            "items": [merchant_summary(r) for r in rows],
            "total": total,
            "page": int(page),
            "page_size": int(limit),
            "has_more": page * int(limit) < total,
        }

    def get_merchant(self, merchant_id: str) -> dict:
        return merchant_detail(fetch_merchant(self.conn, merchant_id))

    def get_recommendations(
        self,
        category: str,
        area: Optional[str] = None,
        limit: int = 5,
        page: int = 1,
    ) -> dict:
        """Top-rated merchants in a category (optionally scoped to an area)."""
        cats = _distinct(self.conn, "merchants", "category")
        if cats and category not in cats:
            raise BadCategoryError(
                "category must be one of " + ", ".join(sorted(cats)))
        if limit is None or limit < 1:
            raise BadArgError("limit must be >= 1")
        if limit > 50:
            limit = 50
        if page is None or page < 1:
            raise BadArgError("page must be >= 1")

        where = ["category = ?"]
        args: List = [category]
        if area:
            where.append("area = ?")
            args.append(area)
        where_sql = " AND ".join(where)
        total = int(self.conn.execute(
            f"SELECT COUNT(*) AS n FROM merchants WHERE {where_sql}", args
        ).fetchone()["n"])
        offset = (page - 1) * int(limit)
        rows = self.conn.execute(
            f"SELECT * FROM merchants WHERE {where_sql} "
            f"ORDER BY rating_tenths DESC, review_count DESC, merchant_id ASC LIMIT ? OFFSET ?",
            args + [int(limit), offset],
        ).fetchall()
        return {
            "items": [merchant_summary(r) for r in rows],
            "total": total,
            "page": int(page),
            "page_size": int(limit),
            "has_more": page * int(limit) < total,
        }
