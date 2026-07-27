from mcp.server.fastmcp import FastMCP

from ..services.saved_service import SavedService
from ._common import dumps, handle_errors


def register_saved_tools(mcp: FastMCP, svc: SavedService) -> None:

    @mcp.tool()
    @handle_errors
    async def save_listing(user_id: str, listing_id: str) -> str:
        """Save (favourite) a listing for a user. Errors LISTING_NOT_FOUND / ALREADY_SAVED."""
        return dumps(svc.save_listing(user_id, listing_id))

    @mcp.tool()
    @handle_errors
    async def unsave_listing(user_id: str, listing_id: str) -> str:
        """Remove a listing from a user's saved set. Errors NOT_SAVED if it was not saved."""
        return dumps(svc.unsave_listing(user_id, listing_id))

    @mcp.tool()
    @handle_errors
    async def list_saved(user_id: str) -> str:
        """List a user's saved listings (summaries, each with saved_at), oldest-saved first."""
        return dumps(svc.list_saved(user_id))
