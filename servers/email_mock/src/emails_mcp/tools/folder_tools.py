"""Folder tools: list / create / delete / stats / unread-count."""
from typing import Optional

from mcp.server.fastmcp import FastMCP

from ..services.folder_service import FolderService
from ._common import dumps, handle_errors


def register_folder_tools(mcp: FastMCP, folder_service: FolderService) -> None:

    @mcp.tool()
    @handle_errors
    async def get_folders() -> str:
        """List every email folder with its total and unread message counts."""
        return dumps({"folders": folder_service.list_folders()})

    @mcp.tool()
    @handle_errors
    async def create_folder(folder_name: str) -> str:
        """Create a new email folder. Fails if a folder with that name already exists."""
        return dumps(folder_service.create_folder(folder_name))

    @mcp.tool()
    @handle_errors
    async def delete_folder(folder_name: str) -> str:
        """Delete a folder and every email in it. System folders (INBOX, Sent, Drafts, Trash, Spam) are protected."""
        return dumps(folder_service.delete_folder(folder_name))

    @mcp.tool()
    @handle_errors
    async def get_mailbox_stats(folder_name: Optional[str] = None) -> str:
        """Return total/unread counts for one folder, or aggregated across all folders if folder_name is omitted."""
        return dumps(folder_service.get_folder_stats(folder_name))

    @mcp.tool()
    @handle_errors
    async def get_unread_count(folder_name: Optional[str] = None) -> str:
        """Return the unread message count for one folder, or aggregated across all folders if folder_name is omitted."""
        return dumps(folder_service.get_unread_count(folder_name))
