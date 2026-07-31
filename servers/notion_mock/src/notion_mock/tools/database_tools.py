from typing import Any, Dict, List, Optional

from mcp.server.fastmcp import FastMCP

from ..services.database_service import DatabaseService
from ._common import dumps, handle_errors


def register_database_tools(mcp: FastMCP, database_service: DatabaseService) -> None:

    @mcp.tool(name="API-post-database-query")
    @handle_errors
    async def post_database_query(
        database_id: str,
        filter: Optional[Dict[str, Any]] = None,
        sorts: Optional[List[Dict[str, Any]]] = None,
        page_size: int = 100,
        start_cursor: Optional[str] = None,
    ) -> str:
        """Query rows in a Notion database. ``filter`` accepts a Notion-style filter object (``{property,<type>:{op:value}}`` plus ``and``/``or`` combinators) — this mock implements ``equals``/``contains``/``starts_with``/``ends_with`` on string-y types, plus ``checkbox.equals`` and numeric comparators. ``sorts`` accepts ``[{property|timestamp, direction}]``. ``start_cursor`` is accepted but ignored."""
        return dumps(
            database_service.query_database(
                database_id=database_id,
                filter_=filter,
                sorts=sorts,
                page_size=page_size,
            )
        )
