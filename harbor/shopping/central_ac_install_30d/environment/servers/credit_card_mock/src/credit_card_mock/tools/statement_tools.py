from mcp.server.fastmcp import FastMCP

from ..services.statement_service import StatementService
from ._common import dumps, handle_errors


def register_statement_tools(mcp: FastMCP, service: StatementService) -> None:

    @mcp.tool()
    @handle_errors
    async def list_statements(card_id: str, limit: int = 12, page: int = 1) -> str:
        """List monthly statements for a card (newest first), paginated.

        Each item has period_start, period_end, opening_balance_minor,
        new_charges_minor, payments_minor, closing_balance_minor,
        min_payment_due_minor, due_date, and status ∈ {open, paid, overdue,
        partial}. Money fields are integer cents (CNY minor units). limit is
        the page size (default 12, max 60); page (>=1) selects which page.
        Returns an envelope {items, total, page, page_size, has_more}; pass
        page=2,3,... while has_more is true to read the full statement set.
        """
        return dumps(service.list_statements(card_id, int(limit), page=page))

    @mcp.tool()
    @handle_errors
    async def get_statement(statement_id: str) -> str:
        """Fetch a single statement's header plus its line items.

        Each statement_line has kind ∈ {purchase, refund, payment, fee,
        interest, adjustment}. Charge amounts are positive; refunds and
        payments are negative.
        """
        return dumps(service.get_statement(statement_id))

    @mcp.tool()
    @handle_errors
    async def list_unbilled(card_id: str) -> str:
        """List transactions posted since the latest statement period_end.

        Same line shape as get_statement's statement_lines minus
        statement_id (these are not on any statement yet).
        """
        return dumps(service.list_unbilled(card_id))
