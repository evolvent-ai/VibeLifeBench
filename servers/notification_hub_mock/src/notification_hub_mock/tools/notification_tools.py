from typing import Optional

from mcp.server.fastmcp import FastMCP

from ..services.notification_service import NotificationService
from ._common import dumps, handle_errors


def register_notification_tools(
    mcp: FastMCP, notification_service: NotificationService
) -> None:

    @mcp.tool()
    @handle_errors
    async def list_notifications(
        user_id: str,
        unread_only: bool = False,
        source: Optional[str] = None,
        since: Optional[str] = None,
        limit: int = 50,
    ) -> str:
        """List a user's inbox notifications, newest first. `unread_only` filters to read=false; `source` filters by platform key; `since` (YYYY-MM-DD) keeps notifications on/after that date; `limit` caps results (max 500). Notifications are static/historical — the server never generates them."""
        return dumps(
            notification_service.list_notifications(
                user_id=user_id,
                unread_only=unread_only,
                source=source,
                since=since,
                limit=limit,
            )
        )

    @mcp.tool()
    @handle_errors
    async def get_notification(notification_id: str) -> str:
        """Return full detail (incl. parsed payload) for one notification. Errors NOTIFICATION_NOT_FOUND if missing."""
        return dumps(notification_service.get_notification(notification_id))

    @mcp.tool()
    @handle_errors
    async def mark_read(notification_id: str) -> str:
        """Mark one notification as read. Idempotent; returns the updated notification."""
        return dumps(notification_service.mark_read(notification_id))

    @mcp.tool()
    @handle_errors
    async def mark_all_read(user_id: str) -> str:
        """Mark all of a user's unread notifications as read. Returns {user_id, marked_read} (count newly flipped)."""
        return dumps(notification_service.mark_all_read(user_id))
