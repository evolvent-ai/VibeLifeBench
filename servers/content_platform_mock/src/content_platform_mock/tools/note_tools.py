from typing import List, Optional

from mcp.server.fastmcp import FastMCP

from ..services.note_service import NoteService
from ._common import dumps, handle_errors


def register_note_tools(mcp: FastMCP, note_service: NoteService) -> None:

    @mcp.tool()
    @handle_errors
    async def search_notes(
        keyword: str,
        category: Optional[str] = None,
        sort: str = "hot",
        limit: Optional[int] = None,
    ) -> str:
        """Search notes (笔记) by keyword over title/body/tags. Optional category filter (备考/装修/健身/旅行/母婴/其他). sort ∈ {hot, latest, most_collected}, default hot. limit defaults to 20, capped at 100. Returns compact note summaries with author and engagement counts."""
        return dumps(
            note_service.search_notes(
                keyword=keyword, category=category, sort=sort, limit=limit
            )
        )

    @mcp.tool()
    @handle_errors
    async def get_note(note_id: str) -> str:
        """Return full detail for a note: title, body text, image_captions (text descriptions, no binaries), tags, author, and like/collect/comment/view counts. NOTE_NOT_FOUND if missing."""
        return dumps(note_service.get_note(note_id))

    @mcp.tool()
    @handle_errors
    async def get_note_comments(note_id: str, limit: Optional[int] = None) -> str:
        """List comments on a note, oldest first. limit defaults to 20, capped at 100. NOTE_NOT_FOUND if the note is missing."""
        return dumps(note_service.get_note_comments(note_id, limit))

    @mcp.tool()
    @handle_errors
    async def post_comment(note_id: str, user_id: str, body: str) -> str:
        """Post a comment as user_id on a note and increment its comment_count. NOTE_NOT_FOUND / USER_NOT_FOUND on bad ids."""
        return dumps(note_service.post_comment(note_id, user_id, body))

    @mcp.tool()
    @handle_errors
    async def get_trending(category: Optional[str] = None, limit: Optional[int] = None) -> str:
        """Return the hottest notes ranked by weighted engagement (likes + 2*collects + 3*comments), each with a 1-based rank. Optional category filter (备考/装修/健身/旅行/母婴/其他). limit defaults to 20, capped at 100."""
        return dumps(note_service.get_trending(category, limit))

    @mcp.tool()
    @handle_errors
    async def publish_note(
        user_id: str,
        title: str,
        body: str,
        tags: Optional[List[str]] = None,
        category: Optional[str] = None,
        image_captions: Optional[List[str]] = None,
    ) -> str:
        """Publish a new note authored by user_id. tags and image_captions are string lists (image_captions are text descriptions only, no binaries). category ∈ {备考,装修,健身,旅行,母婴,其他}, default 其他. Increments the author's note_count and returns the new note_id. USER_NOT_FOUND if the author is missing."""
        return dumps(
            note_service.publish_note(
                user_id=user_id,
                title=title,
                body=body,
                tags=tags,
                category=category,
                image_captions=image_captions,
            )
        )
