"""Agent-facing quote lookup."""
from mcp.server.fastmcp import FastMCP

from ..services.market_service import MarketService
from ._common import dumps, handle_errors


def register_market_tools(mcp: FastMCP, market_service: MarketService) -> None:

    @mcp.tool()
    @handle_errors
    async def get_quote(symbol: str) -> str:
        """Get the latest daily quote for an A-share symbol.

        Args:
            symbol: 6-digit code as a string, e.g. "600519" or "000333".
        Returns JSON: {symbol, name, bid_minor, ask_minor, last_minor,
                       prev_close_minor, day_change_bp, as_of_date}.
        Prices are CNY cents (1 CNY = 100 minor units).
        """
        return dumps(market_service.get_quote(symbol))
