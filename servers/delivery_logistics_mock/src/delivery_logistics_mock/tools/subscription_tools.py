from mcp.server.fastmcp import FastMCP

from ..services.subscription_service import SubscriptionService
from ._common import dumps, handle_errors


def register_subscription_tools(mcp: FastMCP, subs: SubscriptionService) -> None:

    @mcp.tool()
    @handle_errors
    async def subscribe_status(tracking_no: str, channel: str, target: str) -> str:
        """Subscribe to status updates for a shipment.

        ``channel`` is one of {"email", "sms", "webhook"}. ``target`` is the email
        address, phone number, or webhook URL to deliver to. Returns a subscription_id;
        store this if you intend to unsubscribe later.
        """
        return dumps(subs.subscribe_status(tracking_no, channel, target))

    @mcp.tool()
    @handle_errors
    async def unsubscribe(subscription_id: str) -> str:
        """Deactivate a previously-created status subscription.

        Idempotent — calling on an already-inactive subscription returns
        ``already_inactive: true`` rather than an error.
        """
        return dumps(subs.unsubscribe(subscription_id))
