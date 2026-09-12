from mcp.server.fastmcp import FastMCP

from ..services.pickup_service import PickupService
from ._common import dumps, handle_errors


def register_pickup_tools(mcp: FastMCP, pickup: PickupService) -> None:

    @mcp.tool()
    @handle_errors
    async def request_pickup(
        user_id: str,
        pickup_addr: dict,
        dest_addr: dict,
        item_desc: str,
        weight_kg: float,
        service_type: str,
        scheduled_at: str,
    ) -> str:
        """Schedule a carrier pickup and create the shipment in one call.

        Picks the first carrier offer the route would yield (matching estimate_delivery),
        creates a new shipment in status 'label_created' with an initial scan event, and
        queues the pickup. ``service_type`` is {"standard", "express", "same_day"};
        ``scheduled_at`` is an ISO timestamp (date-only YYYY-MM-DD also accepted) and may
        not be in the past. Returns shipment_id, tracking_no, carrier, fee_minor, eta_date.
        """
        return dumps(
            pickup.request_pickup(
                user_id,
                pickup_addr,
                dest_addr,
                item_desc,
                weight_kg,
                service_type,
                scheduled_at,
            )
        )
