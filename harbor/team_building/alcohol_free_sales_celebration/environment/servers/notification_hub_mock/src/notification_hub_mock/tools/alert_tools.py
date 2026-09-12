from mcp.server.fastmcp import FastMCP

from ..services.alert_service import AlertService
from ._common import dumps, handle_errors


def register_alert_tools(mcp: FastMCP, alert_service: AlertService) -> None:

    @mcp.tool()
    @handle_errors
    async def create_price_alert(
        user_id: str, item_ref: str, target_price_minor: int
    ) -> str:
        """Create a target-price watch on an item. `item_ref` is an external product/SKU reference; `target_price_minor` is the trigger price in cents (CNY minor units, must be positive). Recording the alert does NOT fire a notification by itself."""
        return dumps(
            alert_service.create_price_alert(
                user_id=user_id,
                item_ref=item_ref,
                target_price_minor=int(target_price_minor),
            )
        )

    @mcp.tool()
    @handle_errors
    async def list_price_alerts(user_id: str) -> str:
        """List a user's price alerts with status (active/triggered/cancelled) and target_price_minor in cents."""
        return dumps(alert_service.list_price_alerts(user_id))
