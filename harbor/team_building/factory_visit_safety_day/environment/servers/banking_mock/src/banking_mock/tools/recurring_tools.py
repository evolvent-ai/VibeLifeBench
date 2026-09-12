from typing import Optional

from mcp.server.fastmcp import FastMCP

from ..services.recurring_service import RecurringService
from ._common import dumps, handle_errors


def register_recurring_tools(mcp: FastMCP, recurring_service: RecurringService) -> None:

    @mcp.tool()
    @handle_errors
    async def schedule_recurring(
        account_id: str,
        payee_id: str,
        amount_minor: int,
        freq: str,
        start_date: str,
        end_date: Optional[str] = None,
    ) -> str:
        """Schedule a recurring debit from an account to a payee. `freq` is one of `daily`, `weekly`, `monthly`. Dates are YYYY-MM-DD. The first run posts on `start_date`."""
        return dumps(
            recurring_service.schedule_recurring(
                account_id=account_id,
                payee_id=payee_id,
                amount_minor=int(amount_minor),
                freq=freq,
                start_date=start_date,
                end_date=end_date,
            )
        )

    @mcp.tool()
    @handle_errors
    async def cancel_recurring(schedule_id: str) -> str:
        """Cancel an active recurring payment schedule. Returns SCHEDULE_NOT_FOUND if the id is unknown."""
        return dumps(recurring_service.cancel_recurring(schedule_id))

    @mcp.tool()
    @handle_errors
    async def list_recurring(
        user_id: str,
        status_filter: Optional[str] = None,
    ) -> str:
        """List a user's recurring payment schedules. Optional `status_filter` is one of `active`, `paused`, `cancelled`, `ended`."""
        return dumps(
            recurring_service.list_recurring(
                user_id=user_id,
                status_filter=status_filter,
            )
        )
