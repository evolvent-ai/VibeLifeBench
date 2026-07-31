from typing import Any, Dict, List, Optional

from mcp.server.fastmcp import FastMCP

from ..services.block_service import BlockService
from ._common import dumps, handle_errors


def register_block_tools(mcp: FastMCP, block_service: BlockService) -> None:

    @mcp.tool(name="API-get-block-children")
    @handle_errors
    async def get_block_children(
        block_id: str,
        page_size: int = 10000,
        start_cursor: Optional[str] = None,
    ) -> str:
        """List the immediate children of a page or a parent block, ordered top-to-bottom. ``block_id`` accepts either a page id (returns top-level page blocks) or a block id (returns that block's nested children). ``start_cursor`` is accepted but ignored — this mock returns all children in one page."""
        return dumps(block_service.get_block_children(block_id, page_size=page_size))

    @mcp.tool(name="API-patch-block-children")
    @handle_errors
    async def patch_block_children(
        block_id: str,
        children: List[Dict[str, Any]],
        after: Optional[str] = None,
    ) -> str:
        """Append blocks to a page or a parent block. Each child is a block spec like ``{"type":"paragraph","paragraph":{"rich_text":[...]}}``. Nested ``children`` arrays are recursively created. ``after`` is accepted for API parity but ignored — new blocks always append to the end."""
        return dumps(block_service.append_children(block_id, children, after=after))

    @mcp.tool(name="API-retrieve-a-block")
    @handle_errors
    async def retrieve_a_block(block_id: str) -> str:
        """Return a single block by id."""
        return dumps(block_service.retrieve_block(block_id))

    @mcp.tool(name="API-update-a-block")
    @handle_errors
    async def update_a_block(
        block_id: str,
        paragraph: Optional[Dict[str, Any]] = None,
        heading_1: Optional[Dict[str, Any]] = None,
        heading_2: Optional[Dict[str, Any]] = None,
        heading_3: Optional[Dict[str, Any]] = None,
        bulleted_list_item: Optional[Dict[str, Any]] = None,
        numbered_list_item: Optional[Dict[str, Any]] = None,
        to_do: Optional[Dict[str, Any]] = None,
        toggle: Optional[Dict[str, Any]] = None,
        quote: Optional[Dict[str, Any]] = None,
        callout: Optional[Dict[str, Any]] = None,
        code: Optional[Dict[str, Any]] = None,
        archived: Optional[bool] = None,
        type: Optional[str] = None,
    ) -> str:
        """Update a block's type-specific content or archive flag. Pass the type-specific payload under its matching key (e.g. ``paragraph={"rich_text":[{"type":"text","text":{"content":"new"}}]}``). ``archived=true`` archives the block; ``type`` retargets the block type."""
        body: Dict[str, Any] = {}
        for k, v in (
            ("paragraph", paragraph), ("heading_1", heading_1), ("heading_2", heading_2),
            ("heading_3", heading_3), ("bulleted_list_item", bulleted_list_item),
            ("numbered_list_item", numbered_list_item), ("to_do", to_do),
            ("toggle", toggle), ("quote", quote), ("callout", callout), ("code", code),
        ):
            if v is not None:
                body[k] = v
        if archived is not None:
            body["archived"] = archived
        if type is not None:
            body["type"] = type
        return dumps(block_service.update_block(block_id, body))

    @mcp.tool(name="API-delete-a-block")
    @handle_errors
    async def delete_a_block(block_id: str) -> str:
        """Soft-delete a block (sets ``archived=true``). The block id stays resolvable for reads but stops appearing in child listings."""
        return dumps(block_service.delete_block(block_id))
