from typing import Optional

from mcp.server.fastmcp import FastMCP

from ..services.transfer_service import TransferService
from ._common import dumps, handle_errors


def register_transfer_tools(mcp: FastMCP, transfer_service: TransferService) -> None:

    @mcp.tool()
    @handle_errors
    async def transfer(
        from_account_id: str,
        to_account_id: str,
        amount_minor: int,
        memo: Optional[str] = None,
    ) -> str:
        """Move funds between two accounts of the same user. Atomic. Money in minor units (cents). Rejects when the source is frozen (ACCOUNT_FROZEN) or has insufficient balance (INSUFFICIENT_FUNDS). For external recipients use add_payee + pay_payee."""
        return dumps(
            transfer_service.transfer(
                from_account_id=from_account_id,
                to_account_id=to_account_id,
                amount_minor=int(amount_minor),
                memo=memo,
            )
        )
