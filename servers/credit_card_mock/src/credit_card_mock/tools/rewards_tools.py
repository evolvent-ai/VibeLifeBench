from mcp.server.fastmcp import FastMCP

from ..services.rewards_service import RewardsService
from ._common import dumps, handle_errors


def register_rewards_tools(mcp: FastMCP, service: RewardsService) -> None:

    @mcp.tool()
    @handle_errors
    async def get_rewards(card_id: str) -> str:
        """Fetch reward points balance and redemption catalog for a card.

        Returns {points_balance, ytd_earned, lifetime_earned, updated_at,
        recent_earnings, redemption_options}. recent_earnings shows the
        last 10 ledger entries; redemption_options enumerates valid
        redemption_code values usable in redeem_rewards.
        """
        return dumps(service.get_rewards(card_id))

    @mcp.tool()
    @handle_errors
    async def redeem_rewards(card_id: str, redemption_code: str) -> str:
        """Redeem reward points using a code from get_rewards's catalog.

        Deducts the catalog cost from points_balance and writes a redeem
        row to the rewards ledger. Rejects with INSUFFICIENT_POINTS if
        balance is too low and BAD_REDEMPTION if the code is unknown.
        """
        return dumps(service.redeem_rewards(card_id, redemption_code))
