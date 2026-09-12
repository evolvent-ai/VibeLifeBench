from typing import Any, Dict, Optional

from mcp.server.fastmcp import FastMCP

from ..services.search_service import SearchService
from ._common import dumps, handle_errors


def register_search_tools(mcp: FastMCP, search_service: SearchService) -> None:

    @mcp.tool(name="API-post-search")
    @handle_errors
    async def post_search(
        query: Optional[str] = None,
        filter: Optional[Dict[str, Any]] = None,
        sort: Optional[Dict[str, Any]] = None,
        page_size: int = 100,
        start_cursor: Optional[str] = None,
    ) -> str:
        """Search workspace pages and databases by title substring. ``filter={"value":"page"}`` or ``{"value":"database"}`` narrows by object kind. ``sort={"direction":"descending","timestamp":"last_edited_time"}`` orders the result list. Empty/omitted ``query`` returns everything (subject to filter/sort). Results are paginated: ``page_size`` (default 100, max 100) is the page size, and the response carries ``has_more``/``next_cursor`` — pass ``start_cursor=next_cursor`` to read the next page until ``has_more`` is false."""
        return dumps(
            search_service.post_search(
                query=query,
                filter_=filter,
                sort=sort,
                page_size=page_size,
                start_cursor=start_cursor,
            )
        )
