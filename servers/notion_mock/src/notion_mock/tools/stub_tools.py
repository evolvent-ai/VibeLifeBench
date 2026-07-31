"""Stub registrations for low-priority tools.

These return ``{"error":"NOT_IMPLEMENTED","code":"NOT_IMPL"}`` so the
agent gets a clean signal instead of an "unknown tool" error from the
MCP transport layer. See BUILD_REPORT.md §Stubs.
"""
from typing import Any, Dict, Optional

from mcp.server.fastmcp import FastMCP

from ._common import dumps


_STUB_PAYLOAD = {"error": "NOT_IMPLEMENTED", "code": "NOT_IMPL"}


def register_stub_tools(mcp: FastMCP) -> None:

    @mcp.tool(name="API-create-a-database")
    async def create_a_database(
        parent: Optional[Dict[str, Any]] = None,
        title: Optional[Any] = None,
        properties: Optional[Dict[str, Any]] = None,
    ) -> str:
        """Stub: creating databases is intentionally not implemented in the mock. Returns ``{error,code}`` so tasks fail fast and prefer pre-seeded databases."""
        return dumps(_STUB_PAYLOAD)

    @mcp.tool(name="API-retrieve-a-database")
    async def retrieve_a_database(database_id: Optional[str] = None) -> str:
        """Stub: retrieving a database object is not yet implemented; use ``API-post-search`` + ``API-post-database-query`` instead."""
        return dumps(_STUB_PAYLOAD)

    @mcp.tool(name="API-update-a-database")
    async def update_a_database(
        database_id: Optional[str] = None,
        title: Optional[Any] = None,
        properties: Optional[Dict[str, Any]] = None,
    ) -> str:
        """Stub: database schema updates are not implemented in the mock."""
        return dumps(_STUB_PAYLOAD)

    @mcp.tool(name="API-create-a-comment")
    async def create_a_comment(
        parent: Optional[Dict[str, Any]] = None,
        discussion_id: Optional[str] = None,
        rich_text: Optional[Any] = None,
    ) -> str:
        """Stub: comment creation is not implemented in the mock."""
        return dumps(_STUB_PAYLOAD)

    @mcp.tool(name="API-retrieve-a-comment")
    async def retrieve_a_comment(block_id: Optional[str] = None) -> str:
        """Stub: comment retrieval is not implemented in the mock."""
        return dumps(_STUB_PAYLOAD)

    @mcp.tool(name="API-get-user")
    async def get_user(user_id: Optional[str] = None) -> str:
        """Stub: only ``API-get-self`` is implemented in the mock."""
        return dumps(_STUB_PAYLOAD)

    @mcp.tool(name="API-get-users")
    async def get_users() -> str:
        """Stub: listing users is not implemented; use ``API-get-self``."""
        return dumps(_STUB_PAYLOAD)
