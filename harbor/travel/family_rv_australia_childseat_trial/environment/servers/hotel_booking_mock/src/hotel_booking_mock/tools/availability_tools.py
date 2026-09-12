from mcp.server.fastmcp import FastMCP

from ..services.availability_service import AvailabilityService
from ._common import dumps, handle_errors


def register_availability_tools(mcp: FastMCP, availability_service: AvailabilityService) -> None:

    @mcp.tool()
    @handle_errors
    async def get_room_availability(
        hotel_id: str,
        check_in: str,
        check_out: str,
        guests: int,
    ) -> str:
        """List purchasable rate-plan bundles for a hotel and date window.

        Each element corresponds to a (room_type, flavor) composition that has
        inventory on every night in [check_in, check_out).
        """
        results = availability_service.get_room_availability(hotel_id, check_in, check_out, int(guests))
        return dumps(results)
