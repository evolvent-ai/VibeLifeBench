from typing import Optional

from mcp.server.fastmcp import FastMCP

from ..services.merchant_service import MerchantService
from ._common import dumps, handle_errors


def register_merchant_tools(mcp: FastMCP, merchant_service: MerchantService) -> None:

    @mcp.tool()
    @handle_errors
    async def search_merchants(
        category: str,
        city: Optional[str] = None,
        area: Optional[str] = None,
        min_rating: Optional[float] = None,
        price_band: Optional[str] = None,
        sort: str = "rating",
        limit: int = 20,
        page: int = 1,
    ) -> str:
        """Search merchants by category (restaurant/venue/vet/home_service). Optional filters: city, area, min_rating (1.0-5.0), price_band ($/$$/$$$/$$$$). sort ∈ {rating, price_asc, price_desc, review_count} (default rating). limit is the page size (default 20, clamped to 100); page (>=1) selects which page. Returns an envelope {items, total, page, page_size, has_more} of compact merchant summaries incl. rating, avg_price_minor, has_private_room, max_party_size, tags; pass page=2,3,... while has_more is true to read the full result set."""
        return dumps(
            merchant_service.search_merchants(
                category=category,
                city=city,
                area=area,
                min_rating=min_rating,
                price_band=price_band,
                sort=sort,
                limit=limit,
                page=page,
            )
        )

    @mcp.tool()
    @handle_errors
    async def get_merchant(merchant_id: str) -> str:
        """Return full detail for one merchant: rating, review_count, avg_price_minor (cents), price_band, hours, address, phone, tags, has_private_room, max_party_size. Errors MERCHANT_NOT_FOUND."""
        return dumps(merchant_service.get_merchant(merchant_id))

    @mcp.tool()
    @handle_errors
    async def get_recommendations(
        category: str,
        area: Optional[str] = None,
        limit: int = 5,
        page: int = 1,
    ) -> str:
        """Top-rated merchants in a category (restaurant/venue/vet/home_service), optionally scoped to an area. limit is the page size (default 5, clamped to 50); page (>=1) selects which page. Returns an envelope {items, total, page, page_size, has_more} of merchant summaries sorted by rating then review_count; pass page=2,3,... while has_more is true to read the full result set."""
        return dumps(
            merchant_service.get_recommendations(category=category, area=area, limit=limit, page=page)
        )
