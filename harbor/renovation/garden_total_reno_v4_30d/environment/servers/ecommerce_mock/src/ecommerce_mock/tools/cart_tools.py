from mcp.server.fastmcp import FastMCP

from ..services.cart_service import CartService
from ._common import dumps, handle_errors


def register_cart_tools(mcp: FastMCP, cart: CartService) -> None:

    @mcp.tool()
    @handle_errors
    async def get_cart(user_id: str) -> str:
        """Return the current cart for `user_id`: items, subtotal, applied coupons, discount, and total (all in cents)."""
        return dumps(cart.get_cart(user_id))

    @mcp.tool()
    @handle_errors
    async def add_to_cart(user_id: str, product_id: str, sku_id: str, qty: int) -> str:
        """Add `qty` units of a SKU to the user's cart. Returns the recomputed cart view; errors if stock is insufficient."""
        return dumps(cart.add_to_cart(user_id, product_id, sku_id, int(qty)))

    @mcp.tool()
    @handle_errors
    async def update_cart_item(user_id: str, cart_item_id: str, qty: int) -> str:
        """Set the qty of an existing cart item. Passing qty=0 removes the line. Returns the recomputed cart view."""
        return dumps(cart.update_cart_item(user_id, cart_item_id, int(qty)))

    @mcp.tool()
    @handle_errors
    async def remove_from_cart(user_id: str, cart_item_id: str) -> str:
        """Remove a line from the cart. Returns the recomputed cart view."""
        return dumps(cart.remove_from_cart(user_id, cart_item_id))
