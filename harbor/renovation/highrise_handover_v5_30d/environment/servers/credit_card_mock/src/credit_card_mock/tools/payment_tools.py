from mcp.server.fastmcp import FastMCP

from ..services.payment_service import PaymentService
from ._common import dumps, handle_errors


def register_payment_tools(mcp: FastMCP, service: PaymentService) -> None:

    @mcp.tool()
    @handle_errors
    async def make_payment(card_id: str, amount_minor: int, source_hint: str) -> str:
        """Pay down a card's outstanding balance.

        Applies amount_minor (integer cents) to the open statement balance
        first, then to unbilled. source_hint is an opaque string such as
        "acct_checking_main" — recorded but not validated. Returns
        {payment_id, applied_to_statement_minor, applied_to_unbilled_minor,
        new_outstanding_minor}. Rejects with OVERPAYMENT if amount_minor
        exceeds total outstanding, and INVALID_AMOUNT if amount_minor is
        not a positive integer.
        """
        return dumps(service.make_payment(card_id, int(amount_minor), source_hint))
