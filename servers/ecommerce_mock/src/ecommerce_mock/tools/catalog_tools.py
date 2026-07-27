from typing import Optional

from mcp.server.fastmcp import FastMCP

from ..services.catalog_service import CatalogService
from ._common import dumps, handle_errors


def register_catalog_tools(mcp: FastMCP, catalog: CatalogService) -> None:

    @mcp.tool()
    @handle_errors
    async def search_products(
        query: str,
        category: Optional[str] = None,
        filters: Optional[dict] = None,
        sort: Optional[str] = None,
        limit: int = 20,
    ) -> str:
        """Search products by keyword, category, and filters.

        Args:
            query: Keyword matched against product title, brand, and description (case-insensitive substring).
            category: Optional category. Stored values are Chinese labels, e.g. "家电" (home appliances), "母婴" (mother & baby), "服装" (clothing), "食品" (food), "礼品" (gifts).
            filters: Optional dict; supports `max_price_minor`, `min_price_minor`, `brand`, `in_stock_only`, `min_rating`.
            sort: One of `relevance` (default), `price_asc`, `price_desc`, `rating_desc`, `sales_desc`.
            limit: Page size, capped at 100.

        Returns a JSON array of product summaries (price in cents / RMB minor units).
        """
        return dumps(catalog.search_products(query, category, filters, sort, int(limit)))

    @mcp.tool()
    @handle_errors
    async def get_product(product_id: str) -> str:
        """Fetch full details for a product, including SKU list, stock, rating, and return policy."""
        return dumps(catalog.get_product(product_id))
