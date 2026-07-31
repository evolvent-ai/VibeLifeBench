from typing import Optional

from mcp.server.fastmcp import FastMCP

from ..services.listing_service import ListingService
from ._common import dumps, handle_errors


def register_listing_tools(mcp: FastMCP, svc: ListingService) -> None:

    @mcp.tool()
    @handle_errors
    async def search_listings(
        category: str,
        city: Optional[str] = None,
        district: Optional[str] = None,
        min_price_minor: Optional[int] = None,
        max_price_minor: Optional[int] = None,
        min_rooms: Optional[int] = None,
        max_rooms: Optional[int] = None,
        keyword: Optional[str] = None,
        sort: Optional[str] = None,
        limit: int = 20,
    ) -> str:
        """Search active listings. category (required) is one of rent/sale_house/used_car/secondhand. Prices are in cents (¥1=100); for rent they are monthly rent, otherwise total price. Optional filters: city, district, min/max_price_minor, min/max_rooms, keyword (matches title/community/description). sort one of price_asc/price_desc/newest/area_desc (default newest). limit default 20, max 200. Returns a list of listing summaries."""
        return dumps(
            svc.search_listings(
                category=category,
                city=city,
                district=district,
                min_price_minor=min_price_minor,
                max_price_minor=max_price_minor,
                min_rooms=min_rooms,
                max_rooms=max_rooms,
                keyword=keyword,
                sort=sort,
                limit=limit,
            )
        )

    @mcp.tool()
    @handle_errors
    async def get_listing(listing_id: str) -> str:
        """Return the summary view of one listing (price_minor in cents, area, rooms, metro, agent_id, status). Errors LISTING_NOT_FOUND if unknown."""
        return dumps(svc.get_listing(listing_id))

    @mcp.tool()
    @handle_errors
    async def get_listing_detail(listing_id: str) -> str:
        """Return the full listing detail: flexible attrs, photo captions (text), description, owner, and the listing agent object (if any). Errors LISTING_NOT_FOUND."""
        return dumps(svc.get_listing_detail(listing_id))

    @mcp.tool()
    @handle_errors
    async def get_agent(agent_id: str) -> str:
        """Return a listing agent's profile (name, agency, phone, rating, deals_count, service_area). Errors AGENT_NOT_FOUND."""
        return dumps(svc.get_agent(agent_id))

    @mcp.tool()
    @handle_errors
    async def contact_agent(user_id: str, listing_id: str, message: str) -> str:
        """Send a message to the agent of a listing. Records a contact and returns the agent profile. Errors LISTING_NOT_FOUND / LISTING_DELISTED."""
        return dumps(svc.contact_agent(user_id, listing_id, message))

    @mcp.tool()
    @handle_errors
    async def post_listing(
        user_id: str,
        category: str,
        title: str,
        price_minor: int,
        city: str,
        district: Optional[str] = None,
        community: Optional[str] = None,
        area_sqm: Optional[float] = None,
        rooms: Optional[int] = None,
        metro: Optional[str] = None,
        description: Optional[str] = None,
        attrs: Optional[dict] = None,
        photos: Optional[list] = None,
    ) -> str:
        """Self-list a new listing owned by user_id. category one of rent/sale_house/used_car/secondhand; price_minor a positive integer in cents (monthly rent for rent, total price otherwise). attrs is a free-form dict, photos a list of caption strings. Returns the created listing detail. Errors BAD_CATEGORY / BAD_PRICE / BAD_ARG."""
        return dumps(
            svc.post_listing(
                user_id=user_id,
                category=category,
                title=title,
                price_minor=price_minor,
                city=city,
                district=district,
                community=community,
                area_sqm=area_sqm,
                rooms=rooms,
                metro=metro,
                description=description,
                attrs=attrs,
                photos=photos,
            )
        )

    @mcp.tool()
    @handle_errors
    async def delist(listing_id: str, user_id: Optional[str] = None) -> str:
        """Mark a listing as delisted (status='delisted'). If user_id is given it must match the listing's owner_user_id (NOT_OWNER otherwise). Errors LISTING_NOT_FOUND."""
        return dumps(svc.delist(listing_id, user_id))

    @mcp.tool()
    @handle_errors
    async def subscribe_search(user_id: str, query_json: str) -> str:
        """Save a search subscription for a user. query_json is a JSON string of the search criteria; district matches the stored Chinese value, e.g. {"category":"rent","district":"静安区","max_price_minor":1200000} (district "静安区" = Jing'an District). Returns the stored subscription. Errors BAD_ARG if query_json is not valid JSON."""
        return dumps(svc.subscribe_search(user_id, query_json))
