from mcp.server.fastmcp import FastMCP

from ..services.account_service import OfficialAccountService
from ._common import dumps, handle_errors


def register_account_tools(
    mcp: FastMCP, account_service: OfficialAccountService
) -> None:

    @mcp.tool()
    @handle_errors
    async def subscribe_official_account(user_id: str, account_id: str) -> str:
        """Subscribe a user to an official account. Errors ACCOUNT_NOT_FOUND if the account doesn't exist, ALREADY_SUBSCRIBED if already followed."""
        return dumps(
            account_service.subscribe_official_account(user_id, account_id)
        )

    @mcp.tool()
    @handle_errors
    async def list_official_accounts(user_id: str) -> str:
        """List the official accounts a user subscribes to, with subscribed_at."""
        return dumps(account_service.list_official_accounts(user_id))

    @mcp.tool()
    @handle_errors
    async def get_account_feed(account_id: str, limit: int = 20) -> str:
        """Return an official account's feed posts, newest first (max 200). Errors ACCOUNT_NOT_FOUND if the account doesn't exist."""
        return dumps(account_service.get_account_feed(account_id, limit))
