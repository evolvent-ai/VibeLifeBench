from typing import Optional

from mcp.server.fastmcp import FastMCP

from ..services.account_service import AccountService
from ._common import dumps, handle_errors


def register_account_tools(mcp: FastMCP, account_service: AccountService) -> None:

    @mcp.tool()
    @handle_errors
    async def list_accounts(user_id: str) -> str:
        """List all bank accounts owned by a user, with current balance and frozen state."""
        return dumps(account_service.list_accounts(user_id))

    @mcp.tool()
    @handle_errors
    async def get_account(account_id: str) -> str:
        """Return full detail for an account plus a 7-day daily balance trend (one snapshot per day)."""
        return dumps(account_service.get_account(account_id))

    @mcp.tool()
    @handle_errors
    async def list_transactions(
        account_id: str,
        since: Optional[str] = None,
        until: Optional[str] = None,
        limit: int = 50,
        kind_filter: Optional[str] = None,
        page: int = 1,
    ) -> str:
        """List transactions for an account, newest first. Optional date window (YYYY-MM-DD) and kind filter (deposit/withdrawal/transfer_in/transfer_out/payment/fee/interest). limit is the page size (default 50, max 500); page (>=1) selects which page. Returns an envelope {items, total, page, page_size, has_more}; pass page=2,3,... while has_more is true to read the full result set."""
        return dumps(
            account_service.list_transactions(
                account_id=account_id,
                since=since,
                until=until,
                limit=limit,
                kind_filter=kind_filter,
                page=page,
            )
        )
