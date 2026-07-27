from typing import Optional

from mcp.server.fastmcp import FastMCP

from ..services.payee_service import PayeeService
from ._common import dumps, handle_errors


def register_payee_tools(mcp: FastMCP, payee_service: PayeeService) -> None:

    @mcp.tool()
    @handle_errors
    async def list_payees(user_id: str) -> str:
        """List a user's saved external payees. Account numbers are returned masked."""
        return dumps(payee_service.list_payees(user_id))

    @mcp.tool()
    @handle_errors
    async def add_payee(
        user_id: str,
        name: str,
        account_no: str,
        bank_name: str,
    ) -> str:
        """Save a new external payee. The full account number is stored but only the masked form is returned."""
        return dumps(
            payee_service.add_payee(
                user_id=user_id,
                name=name,
                account_no=account_no,
                bank_name=bank_name,
            )
        )

    @mcp.tool()
    @handle_errors
    async def pay_payee(
        account_id: str,
        payee_id: str,
        amount_minor: int,
        memo: Optional[str] = None,
        scheduled_for: Optional[str] = None,
    ) -> str:
        """Pay an external payee from a source account. If `scheduled_for` (YYYY-MM-DD) is a future date the payment is parked as a pending payment and the account is NOT debited yet; otherwise the debit posts immediately."""
        return dumps(
            payee_service.pay_payee(
                account_id=account_id,
                payee_id=payee_id,
                amount_minor=int(amount_minor),
                memo=memo,
                scheduled_for=scheduled_for,
            )
        )
