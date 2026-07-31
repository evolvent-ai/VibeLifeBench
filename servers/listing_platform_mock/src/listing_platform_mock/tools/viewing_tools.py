from mcp.server.fastmcp import FastMCP

from ..services.viewing_service import ViewingService
from ._common import dumps, handle_errors


def register_viewing_tools(mcp: FastMCP, svc: ViewingService) -> None:

    @mcp.tool()
    @handle_errors
    async def schedule_viewing(user_id: str, listing_id: str, datetime: str) -> str:
        """Schedule a viewing of a listing. datetime is ISO-8601 with timezone (e.g. 2026-05-23T15:00:00+08:00). The listing's agent is attached automatically. Errors LISTING_NOT_FOUND / LISTING_DELISTED / BAD_DATE."""
        return dumps(svc.schedule_viewing(user_id, listing_id, datetime))

    @mcp.tool()
    @handle_errors
    async def list_viewings(user_id: str) -> str:
        """List a user's viewings (scheduled and cancelled), earliest scheduled_at first, with the listing title/community."""
        return dumps(svc.list_viewings(user_id))

    @mcp.tool()
    @handle_errors
    async def cancel_viewing(viewing_id: str) -> str:
        """Cancel a scheduled viewing (sets status='cancelled'). Errors VIEWING_NOT_FOUND."""
        return dumps(svc.cancel_viewing(viewing_id))
