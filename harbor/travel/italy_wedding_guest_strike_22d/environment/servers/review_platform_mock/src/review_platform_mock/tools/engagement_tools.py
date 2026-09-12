from mcp.server.fastmcp import FastMCP

from ..services.engagement_service import EngagementService
from ._common import dumps, handle_errors


def register_engagement_tools(mcp: FastMCP, engagement_service: EngagementService) -> None:

    @mcp.tool()
    @handle_errors
    async def get_merchant_qa(merchant_id: str) -> str:
        """List a merchant's Q&A entries, newest first: question, answer (may be null), answered_by, user_id, created_at. Errors MERCHANT_NOT_FOUND."""
        return dumps(engagement_service.get_merchant_qa(merchant_id))

    @mcp.tool()
    @handle_errors
    async def ask_question(user_id: str, merchant_id: str, body: str) -> str:
        """Post a question to a merchant's Q&A. Returns the created entry with answer=null. Errors MERCHANT_NOT_FOUND."""
        return dumps(engagement_service.ask_question(user_id, merchant_id, body))

    @mcp.tool()
    @handle_errors
    async def save_merchant(user_id: str, merchant_id: str) -> str:
        """Save a merchant for a user. Idempotent. Returns {user_id, merchant_id, saved, saved_at}. Errors MERCHANT_NOT_FOUND."""
        return dumps(engagement_service.save_merchant(user_id, merchant_id))

    @mcp.tool()
    @handle_errors
    async def list_saved_merchants(user_id: str) -> str:
        """List the merchants a user has saved, newest first, as merchant summaries with a saved_at field."""
        return dumps(engagement_service.list_saved_merchants(user_id))
