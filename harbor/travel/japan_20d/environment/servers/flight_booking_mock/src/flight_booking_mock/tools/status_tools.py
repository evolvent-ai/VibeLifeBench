"""Flight status + subscription tools."""
from __future__ import annotations

from typing import Any, Optional

from mcp.server.fastmcp import FastMCP

from ..services.status_service import StatusService


def register_status_tools(mcp: FastMCP, status_service: StatusService) -> None:
    @mcp.tool()
    async def get_flight_status(flight_no: str, date: str) -> dict[str, Any]:
        """Real-time(-ish) status for a flight_no on a given date (YYYY-MM-DD)."""
        return status_service.get_flight_status(flight_no, date)

    @mcp.tool()
    async def subscribe_flight_status(
        flight_no: str,
        date: str,
        sink: str = "stdout",
        webhook_url: Optional[str] = None,
    ) -> dict[str, Any]:
        """Subscribe to flight status updates."""
        return status_service.subscribe_flight_status(
            flight_no=flight_no, date=date, sink=sink, webhook_url=webhook_url,
        )
