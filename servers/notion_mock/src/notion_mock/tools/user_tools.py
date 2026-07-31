from mcp.server.fastmcp import FastMCP

from ..services.user_service import UserService
from ._common import dumps, handle_errors


def register_user_tools(mcp: FastMCP, user_service: UserService) -> None:

    @mcp.tool(name="API-get-self")
    @handle_errors
    async def get_self() -> str:
        """Return the bot user representing this integration (i.e. the agent itself). Mirrors Notion's ``GET /v1/users/me``."""
        return dumps(user_service.get_self())
