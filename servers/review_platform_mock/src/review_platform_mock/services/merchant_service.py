"""Merchant discovery: search, detail, recommendations."""
import logging
import sqlite3
from typing import List, Optional

from ..utils.exceptions import BadArgError, BadCategoryError
from ._common import fetch_merchant, merchant_detail, merchant_summary

logger = logging.getLogger(__name__)

VALID_CATEGORIES = ("restaurant", "venue", "vet", "home_service")
VALID_PRICE_BANDS = ("$", "$$", "$$$", "$$$$")
VALID_SORTS = ("rating", "price_asc", "price_desc", "review_count")


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
    ) -> List[dict]:
        if category not in VALID_CATEGORIES:
            raise BadCategoryError(f"category must be one of {VALID_CATEGORIES}")
        if price_band is not None and price_band not in VALID_PRICE_BANDS:
            raise BadArgError(f"price_band must be one of {VALID_PRICE_BANDS}")
        if sort not in VALID_SORTS:
            raise BadArgError(f"sort must be one of {VALID_SORTS}")
        if limit is None or limit < 1:
            raise BadArgError("limit must be >= 1")
        if limit > 100:
            limit = 100

        sql = ["SELECT * FROM merchants WHERE category = ?"]
        args: List = [category]
        if city:
            sql.append("AND city = ?")
            args.append(city)
        if area:
            sql.append("AND area = ?")
            args.append(area)
        if price_band:
            sql.append("AND price_band = ?")
            args.append(price_band)
        if min_rating is not None:
            sql.append("AND rating_tenths >= ?")
            args.append(int(round(float(min_rating) * 10)))

        order = {
            "rating": "rating_tenths DESC, review_count DESC",
            "price_asc": "avg_price_minor ASC",
            "price_desc": "avg_price_minor DESC",
            "review_count": "review_count DESC",
        }[sort]
        sql.append(f"ORDER BY {order}, merchant_id ASC LIMIT ?")
        args.append(int(limit))

        rows = self.conn.execute(" ".join(sql), args).fetchall()
        return [merchant_summary(r) for r in rows]

    def get_merchant(self, merchant_id: str) -> dict:
        return merchant_detail(fetch_merchant(self.conn, merchant_id))

    def get_recommendations(
        self,
        category: str,
        area: Optional[str] = None,
        limit: int = 5,
    ) -> List[dict]:
        """Top-rated merchants in a category (optionally scoped to an area)."""
        if category not in VALID_CATEGORIES:
            raise BadCategoryError(f"category must be one of {VALID_CATEGORIES}")
        if limit is None or limit < 1:
            raise BadArgError("limit must be >= 1")
        if limit > 50:
            limit = 50

        sql = ["SELECT * FROM merchants WHERE category = ?"]
        args: List = [category]
        if area:
            sql.append("AND area = ?")
            args.append(area)
        sql.append(
            "ORDER BY rating_tenths DESC, review_count DESC, merchant_id ASC LIMIT ?"
        )
        args.append(int(limit))
        rows = self.conn.execute(" ".join(sql), args).fetchall()
        return [merchant_summary(r) for r in rows]
