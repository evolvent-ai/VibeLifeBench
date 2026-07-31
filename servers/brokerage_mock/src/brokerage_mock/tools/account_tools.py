"""Agent-facing tools for accounts, portfolio, positions, and performance."""
from mcp.server.fastmcp import FastMCP

from ..services.account_service import AccountService
from ._common import dumps, handle_errors


def register_account_tools(mcp: FastMCP, account_service: AccountService) -> None:

    @mcp.tool()
    @handle_errors
    async def list_accounts(user_id: str) -> str:
        """List all brokerage accounts owned by a user (cash/margin).

        Args:
            user_id: Owning user id, e.g. "usr_li_wei".
        Returns: JSON array of {account_id, broker, account_type, opened_at, status}.
        """
        return dumps(account_service.list_accounts(user_id))

    @mcp.tool()
    @handle_errors
    async def get_portfolio(account_id: str) -> str:
        """Get total portfolio value for an account as of the current sim date.

        Returns JSON with cash_minor, positions_value_minor, total_value_minor,
        todays_pnl_minor, as_of_date. All amounts are CNY cents (1 CNY = 100 minor).
        """
        return dumps(account_service.get_portfolio(account_id))

    @mcp.tool()
    @handle_errors
    async def get_positions(account_id: str) -> str:
        """List all open positions in an account with current market value and P/L.

        Each entry: symbol, name, kind (stock|fund), qty, avg_cost_minor,
        current_price_minor, market_value_minor, unrealized_pnl_minor.
        """
        return dumps(account_service.get_positions(account_id))

    @mcp.tool()
    @handle_errors
    async def get_portfolio_perf(account_id: str, period: str) -> str:
        """Get period return + max drawdown for an account from daily snapshots.

        Args:
            account_id: Brokerage account id.
            period: One of "1d", "7d", "30d", "ytd".
        Returns JSON: {period_return_bp, max_drawdown_bp,
                       start_value_minor, end_value_minor}.
        """
        return dumps(account_service.get_portfolio_perf(account_id, period))
