from typing import Optional

from mcp.server.fastmcp import FastMCP

from ..services.topic_service import TopicService
from ._common import dumps, handle_errors


def register_topic_tools(mcp: FastMCP, topic_service: TopicService) -> None:

    @mcp.tool()
    @handle_errors
    async def search_topics(keyword: str) -> str:
        """Search topics (话题) by name/description, ranked by view_count. Returns topic_id, name, category, note_count and view_count."""
        return dumps(topic_service.search_topics(keyword))

    @mcp.tool()
    @handle_errors
    async def get_topic_feed(topic: str, limit: Optional[int] = None) -> str:
        """Return a topic's metadata plus its notes ranked by engagement. `topic` is the exact topic name (e.g. '考研上岸'). limit defaults to 20, capped at 100. TOPIC_NOT_FOUND if the name is unknown."""
        return dumps(topic_service.get_topic_feed(topic, limit))
