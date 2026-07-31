from typing import Optional

from mcp.server.fastmcp import FastMCP

from ..services.order_service import OrderService
from ._common import dumps, handle_errors


def register_order_tools(mcp: FastMCP, order: OrderService) -> None:

    # ---------------- addresses ----------------
    @mcp.tool()
    @handle_errors
    async def list_addresses(user_id: str) -> str:
        """List the user's shipping addresses, default address first."""
        return dumps(order.list_addresses(user_id))

    @mcp.tool()
    @handle_errors
    async def add_address(
        user_id: str,
        recipient: str,
        phone: str,
        province: str,
        city: str,
        district: str,
        detail: str,
        postal_code: str,
        is_default: bool = False,
    ) -> str:
        """Add a new shipping address. If `is_default` is true, other addresses for the same user are demoted."""
        return dumps(order.add_address(
            user_id, recipient, phone, province, city, district,
            detail, postal_code, bool(is_default),
        ))

    # ---------------- orders ----------------
    @mcp.tool()
    @handle_errors
    async def place_order(
        user_id: str,
        address_id: str,
        payment_method: str,
        note: Optional[str] = None,
    ) -> str:
        """Convert the current cart into a paid order: decrements stock, clears the cart, returns `{order_id, total_minor, item_count, status}`."""
        return dumps(order.place_order(user_id, address_id, payment_method, note))

    @mcp.tool()
    @handle_errors
    async def list_orders(
        user_id: str,
        status_filter: Optional[str] = None,
        limit: int = 20,
    ) -> str:
        """List orders for a user, newest first. `status_filter` may be one of pending_payment | paid | shipped | delivered | completed | refund_requested | refunded | cancelled."""
        return dumps(order.list_orders(user_id, status_filter, int(limit)))

    @mcp.tool()
    @handle_errors
    async def get_order(order_id: str) -> str:
        """Fetch full order detail: header, items, status timeline, and any linked refunds."""
        return dumps(order.get_order(order_id))

    @mcp.tool()
    @handle_errors
    async def cancel_order(order_id: str, reason: str) -> str:
        """Cancel an order. Only allowed when current status is pending_payment or paid; releases reserved stock."""
        return dumps(order.cancel_order(order_id, reason))

    @mcp.tool()
    @handle_errors
    async def track_order(order_id: str) -> str:
        """Return a lightweight tracking view: tracking_no + latest status + updated_at. Full courier timeline lives in the delivery_logistics server."""
        return dumps(order.track_order(order_id))
