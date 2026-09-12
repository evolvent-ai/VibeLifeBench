from mcp.server.fastmcp import FastMCP

from ..services.card_service import CardService
from ._common import dumps, handle_errors


def register_card_tools(mcp: FastMCP, service: CardService) -> None:

    @mcp.tool()
    @handle_errors
    async def list_cards(user_id: str) -> str:
        """List the credit cards belonging to a user.

        Returns a JSON array of card summaries. Each entry includes the
        masked card number, credit limit, currently available credit,
        current statement balance, minimum payment due, due date, and
        status. Money fields are integer cents (CNY minor units).
        """
        return dumps(service.list_cards(user_id))

    @mcp.tool()
    @handle_errors
    async def get_card(card_id: str) -> str:
        """Fetch full detail for a single card.

        Includes billing cycle parameters (cycle_start_day, cycle_end_day,
        grace_period_days), interest APR in basis points, total reward
        points, and the most recent 5 transactions (mix of unbilled +
        statement_lines, newest first).
        """
        return dumps(service.get_card(card_id))

    @mcp.tool()
    @handle_errors
    async def freeze_card(card_id: str) -> str:
        """Freeze a card so new charges are rejected.

        Payments via make_payment still work. Returns the updated card
        summary. Idempotent: freezing an already-frozen card is a no-op.
        """
        return dumps(service.freeze(card_id))

    @mcp.tool()
    @handle_errors
    async def unfreeze_card(card_id: str) -> str:
        """Reactivate a frozen card by flipping its status back to active.

        Returns the updated card summary.
        """
        return dumps(service.unfreeze(card_id))
