"""Agent-facing fund catalog + subscribe / redeem."""
from typing import Optional

from mcp.server.fastmcp import FastMCP

from ..services.fund_service import FundService
from ._common import dumps, handle_errors


def register_fund_tools(mcp: FastMCP, fund_service: FundService) -> None:

    @mcp.tool()
    @handle_errors
    async def list_funds(category: Optional[str] = None) -> str:
        """Browse the fund catalog, optionally filtered by category.

        Args:
            category: Optional one of "money_market", "bond", "equity",
                      "mixed", "index". Null returns all.
        Returns JSON array of {fund_code, fund_name, category, nav_minor,
                               ytd_return_bp, risk_level}.
        """
        return dumps(fund_service.list_funds(category))

    @mcp.tool()
    @handle_errors
    async def get_fund_nav(fund_code: str, lookback_days: int = 30) -> str:
        """Get historical NAV for a fund, newest first.

        Args:
            fund_code: Fund identifier (e.g. "000001").
            lookback_days: How many trailing trading days to return (1..365).
        Returns JSON array of {date, nav_minor}.
        """
        return dumps(fund_service.get_fund_nav(fund_code, int(lookback_days)))

    @mcp.tool()
    @handle_errors
    async def subscribe_fund(account_id: str, fund_code: str, amount_minor: int) -> str:
        """Subscribe to (buy) a fund using cash; units = amount / NAV, rounded down to 0.01.

        Returns JSON: {order_id, status, units_acquired_milli}.
        """
        return dumps(fund_service.subscribe_fund(account_id, fund_code, int(amount_minor)))

    @mcp.tool()
    @handle_errors
    async def redeem_fund(account_id: str, fund_code: str, units_milli: int) -> str:
        """Redeem (sell) `units_milli` thousandths of a fund unit at current NAV.

        Returns JSON: {order_id, status, units_redeemed_milli, proceeds_minor}.
        """
        return dumps(fund_service.redeem_fund(account_id, fund_code, int(units_milli)))
