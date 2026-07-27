"""Management / I/O tools: check_connection, get_email_headers,
download_attachment, export_emails, import_emails."""
from typing import Optional

from mcp.server.fastmcp import FastMCP

from ..services.attachment_service import AttachmentService
from ..services.email_service import EmailService
from ..services.io_service import IOService
from ._common import dumps, handle_errors


def register_management_tools(
    mcp: FastMCP,
    email_service: EmailService,
    attachment_service: AttachmentService,
    io_service: IOService,
) -> None:

    @mcp.tool()
    @handle_errors
    async def check_connection() -> str:
        """Probe the email backend. Always returns ok in the mock — used by agents as a health check."""
        return dumps(email_service.check_connection())

    @mcp.tool()
    @handle_errors
    async def get_email_headers(email_id: str) -> str:
        """Return the technical headers (Message-ID, In-Reply-To, References, raw headers map) for one email."""
        return dumps(email_service.get_email_headers(email_id))

    @mcp.tool()
    @handle_errors
    async def download_attachment(
        email_id: str,
        attachment_filename: str,
        download_path: Optional[str] = None,
    ) -> str:
        """Save an attachment to local disk. download_path defaults to the server's CWD; collisions are auto-renamed."""
        return dumps(
            attachment_service.download_attachment(
                email_id=email_id,
                attachment_filename=attachment_filename,
                download_path=download_path,
            )
        )

    @mcp.tool()
    @handle_errors
    async def export_emails(
        folder: Optional[str] = None,
        export_path: str = "emails_export.json",
        max_emails: Optional[int] = None,
        export_all_folders: bool = False,
    ) -> str:
        """Export emails to a JSON file. Either pick one `folder` (default INBOX) or set export_all_folders=True."""
        return dumps(
            io_service.export_emails(
                folder=folder,
                export_path=export_path,
                max_emails=max_emails,
                export_all_folders=export_all_folders,
            )
        )

    @mcp.tool()
    @handle_errors
    async def import_emails(
        import_path: str,
        target_folder: Optional[str] = None,
        preserve_folders: bool = True,
    ) -> str:
        """Import emails from a JSON file previously written by export_emails. Folders are re-created if missing."""
        return dumps(
            io_service.import_emails(
                import_path=import_path,
                target_folder=target_folder,
                preserve_folders=preserve_folders,
            )
        )
