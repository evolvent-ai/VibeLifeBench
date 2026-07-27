"""Product catalog: search + detail."""
import json
import sqlite3
from typing import List, Optional

from ..utils.exceptions import BadArgError, ProductNotFoundError


ALLOWED_SORTS = {"relevance", "price_asc", "price_desc", "rating_desc", "sales_desc"}


def _thumbnail(product_id: str) -> str:
    return f"https://mock.ecommerce.local/img/{product_id}/main.jpg"


class CatalogService:
    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn

    # ---------------- search ----------------
    def search_products(
        self,
        query: str,
        category: Optional[str] = None,
        filters: Optional[dict] = None,
        sort: Optional[str] = None,
        limit: int = 20,
    ) -> List[dict]:
        filters = filters or {}
        sort_key = sort or "relevance"
        if sort_key not in ALLOWED_SORTS:
            raise BadArgError(f"invalid sort '{sort_key}'")
        try:
            limit = int(limit)
        except Exception:
            raise BadArgError("limit must be an integer")
        limit = max(1, min(limit, 100))

        q = (query or "").strip()
        like = f"%{q}%"

        clauses = []
        params: list = []
        if q:
            clauses.append("(p.title LIKE ? OR p.brand LIKE ? OR p.description LIKE ?)")
            params.extend([like, like, like])
        if category:
            clauses.append("p.category = ?")
            params.append(category)
        if "brand" in filters and filters["brand"]:
            clauses.append("p.brand = ?")
            params.append(filters["brand"])
        if "min_rating" in filters and filters["min_rating"] is not None:
            clauses.append("p.rating >= ?")
            params.append(float(filters["min_rating"]))

        where = ("WHERE " + " AND ".join(clauses)) if clauses else ""

        rows = self.conn.execute(
            f"SELECT p.* FROM products p {where}",
            params,
        ).fetchall()

        results: List[dict] = []
        for p in rows:
            sku_rows = self.conn.execute(
                """
                SELECT s.sku_id, s.price_minor, COALESCE(st.quantity, 0) AS qty
                FROM skus s
                LEFT JOIN stocks st ON st.sku_id = s.sku_id
                WHERE s.product_id = ?
                """,
                (p["product_id"],),
            ).fetchall()
            if not sku_rows:
                continue
            min_sku = min(int(r["price_minor"]) for r in sku_rows)
            max_sku = max(int(r["price_minor"]) for r in sku_rows)
            total_stock = sum(int(r["qty"]) for r in sku_rows)
            in_stock = total_stock > 0

            max_p = filters.get("max_price_minor")
            min_p = filters.get("min_price_minor")
            if max_p is not None and min_sku > int(max_p):
                continue
            if min_p is not None and max_sku < int(min_p):
                continue
            if filters.get("in_stock_only") and not in_stock:
                continue

            results.append({
                "product_id": p["product_id"],
                "title": p["title"],
                "brand": p["brand"],
                "category": p["category"],
                "price_minor": int(p["base_price_minor"]),
                "min_sku_price_minor": min_sku,
                "max_sku_price_minor": max_sku,
                "rating": float(p["rating"]),
                "sales_count": int(p["sales_count"]),
                "in_stock": in_stock,
                "thumbnail_url": _thumbnail(p["product_id"]),
            })

        # ranking
        if sort_key == "price_asc":
            results.sort(key=lambda r: r["min_sku_price_minor"])
        elif sort_key == "price_desc":
            results.sort(key=lambda r: -r["max_sku_price_minor"])
        elif sort_key == "rating_desc":
            results.sort(key=lambda r: (-r["rating"], -r["sales_count"]))
        elif sort_key == "sales_desc":
            results.sort(key=lambda r: -r["sales_count"])
        else:  # relevance: prefer in-stock, then sales
            results.sort(key=lambda r: (not r["in_stock"], -r["sales_count"]))

        return results[:limit]

    # ---------------- detail ----------------
    def get_product(self, product_id: str) -> dict:
        p = self.conn.execute(
            "SELECT * FROM products WHERE product_id = ?", (product_id,)
        ).fetchone()
        if not p:
            raise ProductNotFoundError(f"product {product_id!r} not found")

        sku_rows = self.conn.execute(
            """
            SELECT s.sku_id, s.attrs_json, s.price_minor, COALESCE(st.quantity, 0) AS qty
            FROM skus s
            LEFT JOIN stocks st ON st.sku_id = s.sku_id
            WHERE s.product_id = ?
            ORDER BY s.sku_id
            """,
            (product_id,),
        ).fetchall()

        skus = []
        for r in sku_rows:
            try:
                attrs = json.loads(r["attrs_json"]) if r["attrs_json"] else {}
            except json.JSONDecodeError:
                attrs = {}
            skus.append({
                "sku_id": r["sku_id"],
                "attrs": attrs,
                "price_minor": int(r["price_minor"]),
                "stock": int(r["qty"]),
            })

        return {
            "product_id": p["product_id"],
            "title": p["title"],
            "brand": p["brand"],
            "category": p["category"],
            "description": p["description"],
            "rating": float(p["rating"]),
            "rating_count": int(p["rating_count"]),
            "sales_count": int(p["sales_count"]),
            "skus": skus,
            "reviews_summary": {
                "average_rating": float(p["rating"]),
                "count": int(p["rating_count"]),
            },
            "return_policy": p["return_policy"],
        }
