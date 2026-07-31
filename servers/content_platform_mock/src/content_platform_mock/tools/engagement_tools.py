from mcp.server.fastmcp import FastMCP

from ..services.engagement_service import EngagementService
from ._common import dumps, handle_errors


def register_engagement_tools(mcp: FastMCP, engagement_service: EngagementService) -> None:

    @mcp.tool()
    @handle_errors
    async def like_note(user_id: str, note_id: str) -> str:
        """Like a note as user_id and increment its like_count. Errors: USER_NOT_FOUND, NOTE_NOT_FOUND, ALREADY_EXISTS (already liked)."""
        return dumps(engagement_service.like_note(user_id, note_id))

    @mcp.tool()
    @handle_errors
    async def collect_note(user_id: str, note_id: str) -> str:
        """Save (收藏) a note into the user's collection and increment its collect_count. Errors: USER_NOT_FOUND, NOTE_NOT_FOUND, ALREADY_EXISTS."""
        return dumps(engagement_service.collect_note(user_id, note_id))

    @mcp.tool()
    @handle_errors
    async def uncollect_note(user_id: str, note_id: str) -> str:
        """Remove a note from the user's collection and decrement its collect_count. Errors: USER_NOT_FOUND, NOTE_NOT_FOUND, NOT_COLLECTED."""
        return dumps(engagement_service.uncollect_note(user_id, note_id))

    @mcp.tool()
    @handle_errors
    async def list_collections(user_id: str) -> str:
        """List the notes a user has collected (收藏), most-recently-collected first, each with a collected_at timestamp. USER_NOT_FOUND if missing."""
        return dumps(engagement_service.list_collections(user_id))
