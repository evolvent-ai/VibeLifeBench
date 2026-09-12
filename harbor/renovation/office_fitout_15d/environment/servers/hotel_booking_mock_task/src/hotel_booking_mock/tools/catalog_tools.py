from typing import Optional

from mcp.server.fastmcp import FastMCP

from ..services.catalog_service import CatalogService
from ._common import dumps, handle_errors


def register_catalog_tools(mcp: FastMCP, catalog_service: CatalogService) -> None:

    @mcp.tool()
    @handle_errors
    async def search_hotels(
        city_or_geo: str,
        check_in: str,
        check_out: str,
        guests: int,
        filters: Optional[dict] = None,
        page: int = 1,
    ) -> str:
        """Search hotels in a city, district, or lat,lng;radius_km geo for a date range.

        Args:
            city_or_geo: City name (e.g. "Tokyo", "New York"), a district, or "lat,lng;radius_km".
            check_in: ISO YYYY-MM-DD.
            check_out: ISO YYYY-MM-DD (strictly after check_in, nights <= 30).
            guests: Integer adult headcount, 1..6.
            filters: Optional filter dict (min_star_rating, min_user_rating, max_nightly_price,
                     refundable_only, amenities, breakfast_included, sort, limit, ...).
                `limit` inside filters is the page size (capped at 50).
            page: Which page to return (>= 1). Returns an envelope {items, total,
                page, page_size, has_more}; pass page=2,3,... while has_more is
                true to read the full result set.
        """
        results = catalog_service.search_hotels(city_or_geo, check_in, check_out, int(guests), filters, page=page)
        return dumps(results)

    @mcp.tool()
    @handle_errors
    async def get_hotel_details(hotel_id: str) -> str:
        """Fetch full details for a specific hotel_id."""
        return dumps(catalog_service.get_hotel_details(hotel_id))
