from typing import Optional

from mcp.server.fastmcp import FastMCP

from ..services.catalog_service import CatalogService
from ._common import dumps, handle_errors


def register_catalog_tools(MCP: FastMCP, catalog: CatalogService) -> None:

    @MCP.tool()
    @handle_errors
    async def search_products(
        query: str,
        category: Optional[str] = None,
        filters: Optional[dict] = None,
        sort: Optional[str] = None,
        limit: int = 20,
        page: int = 1,
    ) -> str:
        """Search products by keyword, category, and filters.

        Args:
            query: Keyword matched against product title, brand, and description (case-insensitive substring).
            category: Optional exact-match category. Values are corpus data and
                differ per catalogue, so take one from the `category` field of a
                previous result and pass it back verbatim rather than composing one.
            filters: Optional dict; supports `max_price_minor`, `min_price_minor`, `brand`, `in_stock_only`, `min_rating`.
            sort: One of `relevance` (default), `price_asc`, `price_desc`, `rating_desc`, `sales_desc`.
            limit: Page size, capped at 100.
            page: Which page to return (≥1).

        Returns an envelope {items, total, page, page_size, has_more} of product
        summaries (price in cents / RMB minor units); pass page=2,3,… while
        has_more is true to read the full result set.
        """
        return dumps(catalog.search_products(query, category, filters, sort, int(limit), int(page)))

    @MCP.tool()
    @handle_errors
    async def get_product(product_id: str) -> str:
        """Fetch full details for a product, including SKU list, stock, rating, and return policy."""
        return dumps(catalog.get_product(product_id))
