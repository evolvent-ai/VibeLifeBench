from typing import Optional

from mcp.server.fastmcp import FastMCP

from ..services.topic_service import TopicService
from ._common import dumps, handle_errors


def register_topic_tools(mcp: FastMCP, topic_service: TopicService) -> None:

    @mcp.tool()
    @handle_errors
    async def search_topics(keyword: str) -> str:
        """Search topics by name/description, ranked by view_count. Returns topic_id, name, category, note_count and view_count."""
        return dumps(topic_service.search_topics(keyword))

    @mcp.tool(description=(
        "Return a topic's metadata plus its notes ranked by engagement. "
        "`topic` is the exact topic name as stored, in Chinese \u2014 discover "
        "valid names with search_topics rather than translating one. "
        "Paginated: limit (1-100, default 20) is the page size, page (\u22651) "
        "selects which page. The `notes` field is the current page's items and "
        "total_notes/has_more report completeness; pass page=2,3,\u2026 while "
        "has_more is true to read the full feed. "
        "TOPIC_NOT_FOUND if the name is unknown."
    ))
    @handle_errors
    async def get_topic_feed(topic: str, limit: Optional[int] = None, page: int = 1) -> str:
        """Return a topic's metadata plus its notes ranked by engagement."""
        return dumps(topic_service.get_topic_feed(topic, limit, page))
