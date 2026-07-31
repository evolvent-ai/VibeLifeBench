from mcp.server.fastmcp import FastMCP

from ..services.refund_service import RefundService
from ._common import dumps, handle_errors


def register_refund_tools(mcp: FastMCP, refund: RefundService) -> None:

    @mcp.tool()
    @handle_errors
    async def request_refund(order_id: str, item_id: str, qty: int, reason: str) -> str:
        """Open a refund ticket for `qty` units of a single order item. Returns `{refund_id, status: "submitted", refund_amount_minor, ...}`. Approval happens later via the simulated clock advance."""
        return dumps(refund.request_refund(order_id, item_id, int(qty), reason))
