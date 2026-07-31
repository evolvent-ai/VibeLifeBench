from typing import Any, Dict, List, Optional

from mcp.server.fastmcp import FastMCP

from ..services.page_service import PageService
from ._common import dumps, handle_errors


def register_page_tools(mcp: FastMCP, page_service: PageService) -> None:

    @mcp.tool(name="API-post-page")
    @handle_errors
    async def post_page(
        parent: Dict[str, Any],
        properties: Optional[Dict[str, Any]] = None,
        icon: Optional[Dict[str, Any]] = None,
        cover: Optional[Dict[str, Any]] = None,
        children: Optional[List[Dict[str, Any]]] = None,
    ) -> str:
        """Create a new Notion page or database row. ``parent`` selects the destination — either ``{"type":"page_id","page_id":"..."}``, ``{"type":"database_id","database_id":"..."}``, or ``{"type":"workspace","workspace":true}``. ``properties`` is a Notion-shaped property map (e.g. ``{"title": {"title": [{"type":"text","text":{"content":"..."}}]}}``). Optional ``children`` is an array of block specs appended in order."""
        return dumps(
            page_service.create_page(
                parent=parent,
                properties=properties or {},
                icon=icon,
                cover=cover,
                children=children,
            )
        )

    @mcp.tool(name="API-retrieve-a-page")
    @handle_errors
    async def retrieve_a_page(page_id: str) -> str:
        """Return a page object by id. Works for ordinary pages and for database-row pages (Notion treats DB rows as pages)."""
        return dumps(page_service.retrieve_page(page_id))

    @mcp.tool(name="API-patch-page")
    @handle_errors
    async def patch_page(
        page_id: str,
        properties: Optional[Dict[str, Any]] = None,
        icon: Optional[Dict[str, Any]] = None,
        cover: Optional[Dict[str, Any]] = None,
        archived: Optional[bool] = None,
        in_trash: Optional[bool] = None,
    ) -> str:
        """Update a page's properties / icon / cover, or archive it. ``properties`` is merged into existing properties (set a key to ``null`` to clear it). Set ``archived=true`` or ``in_trash=true`` to soft-delete."""
        return dumps(
            page_service.patch_page(
                page_id=page_id,
                properties=properties,
                icon=icon,
                cover=cover,
                archived=archived,
                in_trash=in_trash,
            )
        )

    @mcp.tool(name="API-retrieve-a-page-property")
    @handle_errors
    async def retrieve_a_page_property(page_id: str, property_id: str) -> str:
        """Return a single property value off a page. ``property_id`` may be the property name (``"title"``, ``"Status"``) or the synthetic id stored on the property object."""
        return dumps(page_service.retrieve_page_property(page_id, property_id))
