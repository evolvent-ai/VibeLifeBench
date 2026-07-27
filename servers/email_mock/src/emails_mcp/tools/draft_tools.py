"""Draft tools: save / get_drafts / update / delete."""
from typing import Optional

from mcp.server.fastmcp import FastMCP

from ..services.draft_service import DraftService
from ._common import dumps, handle_errors


def register_draft_tools(mcp: FastMCP, draft_service: DraftService) -> None:

    @mcp.tool()
    @handle_errors
    async def save_draft(
        subject: str,
        body: str,
        html_body: Optional[str] = None,
        to: Optional[str] = None,
        cc: Optional[str] = None,
        bcc: Optional[str] = None,
        in_reply_to: Optional[str] = None,
    ) -> str:
        """Save a new email draft. `in_reply_to` binds it to a source Message-ID."""
        return dumps(
            draft_service.save_draft(
                subject=subject, body=body, html_body=html_body, to=to, cc=cc, bcc=bcc,
                in_reply_to=in_reply_to
            )
        )

    @mcp.tool()
    @handle_errors
    async def get_drafts(page: int = 1, page_size: int = 20) -> str:
        """List saved drafts, most-recently-updated first."""
        return dumps(draft_service.get_drafts(page=page, page_size=page_size))

    @mcp.tool()
    @handle_errors
    async def update_draft(
        draft_id: str,
        subject: Optional[str] = None,
        body: Optional[str] = None,
        html_body: Optional[str] = None,
        to: Optional[str] = None,
        cc: Optional[str] = None,
        bcc: Optional[str] = None,
        in_reply_to: Optional[str] = None,
    ) -> str:
        """Update fields on an existing draft. Only the supplied fields change."""
        return dumps(
            draft_service.update_draft(
                draft_id=draft_id,
                subject=subject,
                body=body,
                html_body=html_body,
                to=to,
                cc=cc,
                bcc=bcc,
                in_reply_to=in_reply_to,
            )
        )

    @mcp.tool()
    @handle_errors
    async def delete_draft(draft_id: str) -> str:
        """Permanently delete a draft by id."""
        return dumps(draft_service.delete_draft(draft_id))
