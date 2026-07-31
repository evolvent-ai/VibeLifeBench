from mcp.server.fastmcp import FastMCP

from ..services.shipment_service import ShipmentService
from ._common import dumps, handle_errors


def register_shipment_tools(mcp: FastMCP, ship: ShipmentService) -> None:

    @mcp.tool()
    @handle_errors
    async def get_shipment(shipment_id: str) -> str:
        """Return the full record for a shipment by shipment_id.

        Includes sender, recipient, carrier, service level, weight, declared value, fee,
        ETA, every scan event, and any active subscriptions. Use track_package if you
        only have a tracking number.
        """
        return dumps(ship.get_shipment(shipment_id))

    @mcp.tool()
    @handle_errors
    async def estimate_delivery(
        origin_addr: dict,
        dest_addr: dict,
        weight_kg: float,
        service_type: str,
    ) -> str:
        """Estimate carrier offers (fee in cents and ETA) for a hypothetical shipment.

        ``service_type`` must be one of {"standard", "express", "same_day"}. Returns 2-3
        deterministic carrier quotes (carrier, service_level, eta_date, fee_minor); the
        same inputs always produce the same offers. Addresses require recipient, phone,
        province, city, district, and detail.
        """
        return dumps(ship.estimate_delivery(origin_addr, dest_addr, weight_kg, service_type))

    @mcp.tool()
    @handle_errors
    async def reschedule_delivery(
        tracking_no: str,
        new_date: str,
        time_window: str,
    ) -> str:
        """Reschedule an in-flight delivery to a new date and time window.

        Valid only when status is in_transit, out_for_delivery, or exception. ``new_date``
        is ISO YYYY-MM-DD and must not be in the past. ``time_window`` is one of
        {"morning", "afternoon", "evening", "anytime"}. Returns a confirmation_code.
        """
        return dumps(ship.reschedule_delivery(tracking_no, new_date, time_window))

    @mcp.tool()
    @handle_errors
    async def change_address(tracking_no: str, new_address: dict) -> str:
        """Update the recipient address on a shipment that has not yet left the origin hub.

        Allowed only while status is label_created or picked_up; once the package is
        in_transit or later the carrier locks the destination (returns IN_TRANSIT_LOCKED).
        Address requires recipient, phone, province, city, district, and detail.
        """
        return dumps(ship.change_address(tracking_no, new_address))

    @mcp.tool()
    @handle_errors
    async def cancel_shipment(tracking_no: str, reason: str) -> str:
        """Cancel a shipment before it leaves the origin hub.

        Allowed only while status is label_created or picked_up. Once in_transit or later
        the operation fails with CANCEL_TOO_LATE. Any pending pickup is also cancelled.
        """
        return dumps(ship.cancel_shipment(tracking_no, reason))
