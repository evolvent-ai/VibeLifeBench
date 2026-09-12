from mcp.server.fastmcp import FastMCP

from ..services.coupon_service import CouponService
from ._common import dumps, handle_errors


def register_coupon_tools(mcp: FastMCP, coupon: CouponService) -> None:

    @mcp.tool()
    @handle_errors
    async def apply_coupon(user_id: str, code: str) -> str:
        """Apply a coupon code to the user's cart. Returns the recomputed cart view, or an error envelope on validation failure (invalid, expired, below min spend, category mismatch)."""
        return dumps(coupon.apply_coupon(user_id, code))

    @mcp.tool()
    @handle_errors
    async def remove_coupon(user_id: str, code: str) -> str:
        """Detach a previously applied coupon. Returns the recomputed cart view."""
        return dumps(coupon.remove_coupon(user_id, code))
