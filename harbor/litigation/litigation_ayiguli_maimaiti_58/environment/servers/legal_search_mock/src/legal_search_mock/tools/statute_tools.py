from typing import Optional

from mcp.server.fastmcp import FastMCP

from ..services.statute_service import StatuteService
from ._common import dumps, handle_errors


def register_statute_tools(mcp: FastMCP, statute_service: StatuteService) -> None:

    @mcp.tool(description=(
        "Search laws and regulations by keyword (matches name/short "
        "name/summary), newest effective_date first. Paginated: limit (1-100, "
        "default 20) is the page size, page (≥1) selects which page. Returns "
        "an envelope {items, total, page, page_size, has_more}; pass "
        "page=2,3,… while has_more is true to read the full result set. The "
        "result's status field is corpus data, reported verbatim."
    ))
    @handle_errors
    async def search_statutes(
        keyword: Optional[str] = None, limit: int = 20, page: int = 1
    ) -> str:
        """Search laws and regulations by keyword, newest effective_date first."""
        return dumps(
            statute_service.search_statutes(keyword=keyword, limit=limit, page=page)
        )

    @mcp.tool(description=(
        "Return statute metadata plus article_count. "
        "status is a stored Chinese label, returned verbatim: "
        "status is corpus data, reported verbatim. "
        "Errors STATUTE_NOT_FOUND."
    ))
    @handle_errors
    async def get_statute(statute_id: str) -> str:
        """Return statute metadata plus article_count."""
        return dumps(statute_service.get_statute(statute_id))

    @mcp.tool()
    @handle_errors
    async def list_statute_articles(statute_id: str) -> str:
        """List a statute's articles (article_id/article_no/heading) in document order. Use get_article for full text. Errors STATUTE_NOT_FOUND."""
        return dumps(statute_service.list_statute_articles(statute_id))

    @mcp.tool()
    @handle_errors
    async def get_article(article_id: str) -> str:
        """Return the full text of a single statute article plus its statute_name and article_no. Errors ARTICLE_NOT_FOUND."""
        return dumps(statute_service.get_article(article_id))
