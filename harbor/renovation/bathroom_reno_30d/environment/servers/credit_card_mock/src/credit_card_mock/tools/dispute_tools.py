from typing import Optional

from mcp.server.fastmcp import FastMCP

from ..services.dispute_service import DisputeService
from ._common import dumps, handle_errors


def register_dispute_tools(mcp: FastMCP, service: DisputeService) -> None:

    @mcp.tool()
    @handle_errors
    async def dispute_transaction(tx_id: str, reason: str) -> str:
        """Open a dispute against a transaction (unbilled tx_id or billed line_id).

        Disputes start in status "under_review" with an
        expected_resolution_date 30 days out. Returns {dispute_id, status,
        expected_resolution_date}. Rejects with DISPUTE_ALREADY_OPEN if an
        active dispute already exists for the same transaction.
        """
        return dumps(service.dispute_transaction(tx_id, reason))

    @mcp.tool()
    @handle_errors
    async def list_disputes(card_id: str, status_filter: Optional[str] = None) -> str:
        """List disputes on a card, newest first.

        status_filter, when supplied, restricts to one of {under_review,
        approved, denied, withdrawn}.
        """
        return dumps(service.list_disputes(card_id, status_filter))
