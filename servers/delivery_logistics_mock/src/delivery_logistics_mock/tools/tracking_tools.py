from typing import Optional

from mcp.server.fastmcp import FastMCP

from ..services.tracking_service import TrackingService
from ._common import dumps, handle_errors


def register_tracking_tools(mcp: FastMCP, tracking: TrackingService) -> None:

    @mcp.tool()
    @handle_errors
    async def track_package(tracking_no: str) -> str:
        """Look up the live status, ETA, and full event timeline for a tracking number.

        Returns the carrier, current status (label_created / picked_up / in_transit /
        out_for_delivery / delivered / exception / returned / cancelled), the most recent
        scan event, origin and destination cities, the current ETA date, and the ordered
        list of all scan events.
        """
        return dumps(tracking.track_package(tracking_no))

    @mcp.tool()
    @handle_errors
    async def list_shipments(
        user_id: str,
        status_filter: Optional[str] = None,
        limit: int = 20,
    ) -> str:
        """List a user's shipments, newest first.

        Optional ``status_filter`` narrows by a single status code. ``limit`` caps the
        result count (default 20). Each item is a compact summary; call get_shipment for
        full detail.
        """
        return dumps(tracking.list_shipments(user_id, status_filter, limit))
