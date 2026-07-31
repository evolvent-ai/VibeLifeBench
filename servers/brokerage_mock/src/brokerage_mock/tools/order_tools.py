"""Agent-facing order placement and management."""
from typing import Optional

from mcp.server.fastmcp import FastMCP

from ..services.order_service import OrderService
from ._common import dumps, handle_errors


def register_order_tools(mcp: FastMCP, order_service: OrderService) -> None:

    @mcp.tool()
    @handle_errors
    async def list_orders(
        account_id: str,
        status_filter: Optional[str] = None,
        limit: int = 50,
    ) -> str:
        """List orders for an account, newest first.

        Args:
            account_id: Brokerage account id.
            status_filter: Optional - "pending" | "filled" | "cancelled" | "rejected".
            limit: Max rows to return (1..500, default 50).
        Returns JSON array of order dicts.
        """
        return dumps(order_service.list_orders(account_id, status_filter, int(limit)))

    @mcp.tool()
    @handle_errors
    async def place_order(
        account_id: str,
        symbol: str,
        side: str,
        qty: int,
        order_type: str,
        limit_price_minor: Optional[int] = None,
        tif: str = "day",
    ) -> str:
        """Place a stock order. Validates funds (buy) / holdings (sell).

        Market orders fill immediately at the latest close. Limit orders fill
        if the limit crosses today's price; otherwise they queue as pending
        until the next admin sim-day advance.

        Args:
            account_id: Brokerage account id.
            symbol: 6-digit A-share code.
            side: "buy" or "sell".
            qty: Whole-share positive integer.
            order_type: "market" or "limit".
            limit_price_minor: Required for limit; price in CNY cents.
            tif: Time-in-force ("day" only in v1).
        Returns JSON: {order_id, status, fill_price_minor?}.
        """
        return dumps(order_service.place_order(
            account_id=account_id,
            symbol=symbol,
            side=side,
            qty=int(qty),
            order_type=order_type,
            limit_price_minor=int(limit_price_minor) if limit_price_minor is not None else None,
            tif=tif,
        ))

    @mcp.tool()
    @handle_errors
    async def cancel_order(order_id: str) -> str:
        """Cancel a pending order. Errors if the order is already filled or cancelled."""
        return dumps(order_service.cancel_order(order_id))
