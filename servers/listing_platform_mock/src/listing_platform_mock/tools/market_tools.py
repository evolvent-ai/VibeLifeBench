from mcp.server.fastmcp import FastMCP

from ..services.market_service import MarketService
from ._common import dumps, handle_errors


def register_market_tools(mcp: FastMCP, svc: MarketService) -> None:

    @mcp.tool()
    @handle_errors
    async def get_market_stats(area_or_community: str) -> str:
        """Return market transaction statistics for an area or community. Matches area exactly first, then falls back to a substring match. Each row has avg_price_minor (cents), unit (per_month/total/per_sqm), sample_size and period. Errors STATS_NOT_FOUND if nothing matches."""
        return dumps(svc.get_market_stats(area_or_community))
