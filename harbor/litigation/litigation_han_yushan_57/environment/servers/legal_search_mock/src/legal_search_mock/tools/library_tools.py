from mcp.server.fastmcp import FastMCP

from ..services.library_service import LibraryService
from ._common import dumps, handle_errors


def register_library_tools(mcp: FastMCP, library_service: LibraryService) -> None:

    @mcp.tool()
    @handle_errors
    async def save_case(user_id: str, case_id: str) -> str:
        """Save a case to a user's library. Idempotent — re-saving returns the existing entry. Errors CASE_NOT_FOUND."""
        return dumps(library_service.save_case(user_id, case_id))

    @mcp.tool()
    @handle_errors
    async def list_saved(user_id: str) -> str:
        """List a user's saved cases (oldest first), each with its note and an embedded compact case summary."""
        return dumps(library_service.list_saved(user_id))

    @mcp.tool()
    @handle_errors
    async def add_note_to_case(user_id: str, case_id: str, note: str) -> str:
        """Attach (or replace) a free-text note on a user's saved case. Auto-saves the case first if not already saved. Errors CASE_NOT_FOUND."""
        return dumps(library_service.add_note_to_case(user_id, case_id, note))
