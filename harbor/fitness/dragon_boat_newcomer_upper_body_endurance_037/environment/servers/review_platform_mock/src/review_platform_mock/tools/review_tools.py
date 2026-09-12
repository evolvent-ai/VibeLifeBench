from typing import List, Optional

from mcp.server.fastmcp import FastMCP

from ..services.review_service import ReviewService
from ._common import dumps, handle_errors


def register_review_tools(mcp: FastMCP, review_service: ReviewService) -> None:

    @mcp.tool()
    @handle_errors
    async def list_reviews(merchant_id: str, limit: int = 20, page: int = 1) -> str:
        """List reviews for a merchant, newest first. limit is the page size (default 20, clamped to 200); page (>=1) selects which page. Returns an envelope {items, total, page, page_size, has_more}; pass page=2,3,... while has_more is true. Each review has rating (1-5), body, image_captions (list), user_id, created_at. Errors MERCHANT_NOT_FOUND."""
        return dumps(review_service.list_reviews(merchant_id, limit=limit, page=page))

    @mcp.tool()
    @handle_errors
    async def write_review(
        user_id: str,
        merchant_id: str,
        rating: int,
        body: str,
        image_captions: Optional[List[str]] = None,
    ) -> str:
        """Post a review for a merchant. rating is an integer 1-5; body is required; image_captions is an optional list of photo captions. Recomputes the merchant's aggregate rating and returns the new rating + review_count. Errors BAD_RATING, MERCHANT_NOT_FOUND."""
        return dumps(
            review_service.write_review(
                user_id=user_id,
                merchant_id=merchant_id,
                rating=rating,
                body=body,
                image_captions=image_captions,
            )
        )
