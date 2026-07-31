from mcp.server.fastmcp import FastMCP

from ..services.alert_service import AlertService
from ._common import dumps, handle_errors


def register_alert_tools(mcp: FastMCP, alert_service: AlertService) -> None:

    @mcp.tool()
    @handle_errors
    async def list_health_alerts(user_id: str, limit: int = 50) -> str:
        """List recorded readings that fall outside a typical reference range (newest first), with neutral descriptive flags (above_typical_range / below_typical_range) and the reference bounds. Informational only: NOT a medical diagnosis and contains no treatment or medication advice. limit default 50, max 200."""
        return dumps(alert_service.list_health_alerts(user_id=user_id, limit=limit))
