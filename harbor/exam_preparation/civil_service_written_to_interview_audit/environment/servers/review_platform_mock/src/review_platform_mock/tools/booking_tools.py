from typing import Optional

from mcp.server.fastmcp import FastMCP

from ..services.booking_service import BookingService
from ._common import dumps, handle_errors


def register_booking_tools(mcp: FastMCP, booking_service: BookingService) -> None:

    @mcp.tool()
    @handle_errors
    async def list_merchant_deals(merchant_id: str) -> str:
        """List group-buy deals offered by a merchant: title, price_minor, list_price_minor (cents), serves, valid_until, status (active/sold_out/expired). Errors MERCHANT_NOT_FOUND."""
        return dumps(booking_service.list_merchant_deals(merchant_id))

    @mcp.tool()
    @handle_errors
    async def get_deal(deal_id: str) -> str:
        """Return full detail for one group-buy deal. Errors DEAL_NOT_FOUND."""
        return dumps(booking_service.get_deal(deal_id))

    @mcp.tool()
    @handle_errors
    async def reserve(
        user_id: str,
        merchant_id: str,
        datetime: str,
        party_size: int,
        deal_id: Optional[str] = None,
    ) -> str:
        """Book a table reservation at a merchant. datetime is ISO YYYY-MM-DDTHH:MM[:SS]; party_size a positive int (must not exceed the merchant's max_party_size); deal_id optionally attaches an active group-buy deal. Returns the confirmed reservation. Errors BAD_DATE, MERCHANT_NOT_FOUND, PARTY_SIZE_EXCEEDED, DEAL_NOT_FOUND, DEAL_UNAVAILABLE."""
        return dumps(
            booking_service.reserve(
                user_id=user_id,
                merchant_id=merchant_id,
                datetime=datetime,
                party_size=party_size,
                deal_id=deal_id,
            )
        )

    @mcp.tool()
    @handle_errors
    async def list_reservations(user_id: str) -> str:
        """List a user's reservations, newest first, with merchant_name, datetime, party_size, deal_id, and status (confirmed/cancelled)."""
        return dumps(booking_service.list_reservations(user_id))

    @mcp.tool()
    @handle_errors
    async def cancel_reservation(reservation_id: str) -> str:
        """Cancel a reservation by id. Idempotent: returns status 'cancelled' even if already cancelled. Errors RESERVATION_NOT_FOUND."""
        return dumps(booking_service.cancel_reservation(reservation_id))
