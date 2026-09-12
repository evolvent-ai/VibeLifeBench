from mcp.server.fastmcp import FastMCP

from ..services.user_service import UserService
from ._common import dumps, handle_errors


def register_user_tools(mcp: FastMCP, user_service: UserService) -> None:

    @mcp.tool()
    @handle_errors
    async def get_user_profile(user_id: str) -> str:
        """Return a user's profile: handle, nickname, bio, official flag, follower/following/note counts, join date. USER_NOT_FOUND if missing."""
        return dumps(user_service.get_user_profile(user_id))

    @mcp.tool()
    @handle_errors
    async def list_user_notes(user_id: str) -> str:
        """List all notes authored by a user, newest first, as compact summaries. USER_NOT_FOUND if the user is missing."""
        return dumps(user_service.list_user_notes(user_id))

    @mcp.tool()
    @handle_errors
    async def follow_user(user_id: str, target_user_id: str) -> str:
        """Make user_id follow target_user_id and bump the target's follower_count. Errors: SELF_FOLLOW, USER_NOT_FOUND, ALREADY_EXISTS (already following)."""
        return dumps(user_service.follow_user(user_id, target_user_id))

    @mcp.tool()
    @handle_errors
    async def unfollow_user(user_id: str, target_user_id: str) -> str:
        """Make user_id unfollow target_user_id and decrement the target's follower_count. Errors: USER_NOT_FOUND, NOT_FOLLOWING."""
        return dumps(user_service.unfollow_user(user_id, target_user_id))
