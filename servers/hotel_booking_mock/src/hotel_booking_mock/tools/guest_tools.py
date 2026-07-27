from mcp.server.fastmcp import FastMCP

from ..services.guest_service import GuestService
from ._common import dumps, handle_errors


def register_guest_tools(mcp: FastMCP, guest_service: GuestService) -> None:

    @mcp.tool()
    @handle_errors
    async def request_late_checkout(reservation_id: str, new_time: str) -> str:
        """Request a late checkout. new_time is 24-hour HH:MM; fee/approval per SPEC."""
        return dumps(guest_service.request_late_checkout(reservation_id, new_time))

    @mcp.tool()
    @handle_errors
    async def submit_special_request(reservation_id: str, text: str) -> str:
        """Submit a free-form special request; auto-classified into a status bucket."""
        return dumps(guest_service.submit_special_request(reservation_id, text))

    @mcp.tool()
    @handle_errors
    async def get_user_bookings_summary(user_id: str) -> str:
        """Aggregate view of a user's bookings (totals, upcoming, nominal loyalty points)."""
        return dumps(guest_service.get_user_bookings_summary(user_id))
