from typing import Optional, Union

from mcp.server.fastmcp import FastMCP

from ..services.subscription_service import SubscriptionService
from ._common import dumps, handle_errors


def register_subscription_tools(
    mcp: FastMCP, subscription_service: SubscriptionService
) -> None:

    @mcp.tool()
    @handle_errors
    async def list_subscriptions(user_id: str, status: Optional[str] = None) -> str:
        """List a user's cross-platform subscriptions. Optional status filter (active/paused/deleted); when omitted, deleted ones are excluded."""
        return dumps(subscription_service.list_subscriptions(user_id, status))

    @mcp.tool()
    @handle_errors
    async def get_subscription(subscription_id: str) -> str:
        """Return full detail for one subscription. Errors SUBSCRIPTION_NOT_FOUND if missing."""
        return dumps(subscription_service.get_subscription(subscription_id))

    @mcp.tool()
    @handle_errors
    async def create_subscription(
        user_id: str,
        source: str,
        type: str,
        target: str,
        condition_json: Optional[Union[str, dict]] = None,
    ) -> str:
        """Record a new subscription (intent only — never auto-fires notifications). `type` is one of price_drop/restock/policy_update/new_content/price_target/keyword. `source` is the originating platform key (e.g. ecommerce, listing_platform, content_platform, gov_policy). `target` is the watched object (item ref, keyword, account, policy topic). `condition_json` is an optional JSON string (e.g. {"target_price_minor": 29900})."""
        return dumps(
            subscription_service.create_subscription(
                user_id=user_id,
                source=source,
                type=type,
                target=target,
                condition_json=condition_json,
            )
        )

    @mcp.tool()
    @handle_errors
    async def update_subscription(
        subscription_id: str,
        target: Optional[str] = None,
        source: Optional[str] = None,
        condition_json: Optional[Union[str, dict]] = None,
    ) -> str:
        """Update a subscription's target, source, and/or condition_json (a JSON string or object). At least one field must be provided."""
        return dumps(
            subscription_service.update_subscription(
                subscription_id=subscription_id,
                target=target,
                source=source,
                condition_json=condition_json,
            )
        )

    @mcp.tool()
    @handle_errors
    async def pause_subscription(subscription_id: str) -> str:
        """Pause a subscription (status -> paused). Idempotent; returns the updated subscription."""
        return dumps(subscription_service.pause_subscription(subscription_id))

    @mcp.tool()
    @handle_errors
    async def resume_subscription(subscription_id: str) -> str:
        """Resume a paused subscription (status -> active). Idempotent; returns the updated subscription."""
        return dumps(subscription_service.resume_subscription(subscription_id))

    @mcp.tool()
    @handle_errors
    async def delete_subscription(subscription_id: str) -> str:
        """Soft-delete a subscription (status -> deleted). It stops appearing in the default list. Returns the updated subscription."""
        return dumps(subscription_service.delete_subscription(subscription_id))
