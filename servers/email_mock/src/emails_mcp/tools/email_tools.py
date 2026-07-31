"""Email-message tools: get / read / search / send / reply / forward /
delete / move / mark."""
from typing import List, Optional

from mcp.server.fastmcp import FastMCP

from ..services.email_service import EmailService
from ._common import dumps, handle_errors


def register_email_tools(mcp: FastMCP, email_service: EmailService) -> None:

    @mcp.tool()
    @handle_errors
    async def get_emails(folder: str = "INBOX", page: int = 1, page_size: int = 20) -> str:
        """Get a paginated list of emails in a folder (newest first). Returns metadata only — call read_email for the body."""
        return dumps(email_service.get_emails(folder=folder, page=page, page_size=page_size))

    @mcp.tool()
    @handle_errors
    async def read_email(email_id: str) -> str:
        """Read the full body and metadata of one email by id. Marks the email as read."""
        return dumps(email_service.read_email(email_id))

    @mcp.tool()
    @handle_errors
    async def search_emails(
        query: str,
        folder: Optional[str] = None,
        page: int = 1,
        page_size: int = 20,
    ) -> str:
        """Search emails by substring across subject, from_addr, and body_text. Optionally scope to one folder."""
        return dumps(
            email_service.search_emails(
                query=query, folder=folder, page=page, page_size=page_size
            )
        )

    @mcp.tool()
    @handle_errors
    async def send_email(
        to: str,
        subject: str,
        body: str,
        html_body: Optional[str] = None,
        cc: Optional[str] = None,
        bcc: Optional[str] = None,
    ) -> str:
        """Send an email. `to`/`cc`/`bcc` are comma-separated lists. The message is filed in the Sent folder."""
        return dumps(
            email_service.send_email(
                to=to,
                subject=subject,
                body=body,
                html_body=html_body,
                cc=cc,
                bcc=bcc,
            )
        )

    @mcp.tool()
    @handle_errors
    async def reply_email(
        email_id: str,
        body: str,
        html_body: Optional[str] = None,
        cc: Optional[str] = None,
        bcc: Optional[str] = None,
        reply_all: bool = False,
    ) -> str:
        """Reply to an email. Quotes the original message body. Set reply_all=True to include the original CC list."""
        return dumps(
            email_service.reply_email(
                email_id=email_id,
                body=body,
                html_body=html_body,
                cc=cc,
                bcc=bcc,
                reply_all=reply_all,
            )
        )

    @mcp.tool()
    @handle_errors
    async def forward_email(
        email_id: str,
        to: str,
        body: Optional[str] = None,
        html_body: Optional[str] = None,
        cc: Optional[str] = None,
        bcc: Optional[str] = None,
    ) -> str:
        """Forward an email to other recipients. Original attachments are carried over."""
        return dumps(
            email_service.forward_email(
                email_id=email_id,
                to=to,
                body=body,
                html_body=html_body,
                cc=cc,
                bcc=bcc,
            )
        )

    @mcp.tool()
    @handle_errors
    async def delete_email(email_id: str) -> str:
        """Permanently delete an email by id (also removes its attachments)."""
        return dumps(email_service.delete_email(email_id))

    @mcp.tool()
    @handle_errors
    async def delete_emails(email_ids: List[str]) -> str:
        """Delete multiple emails in one call. Returns the per-id success/failure breakdown."""
        return dumps(email_service.delete_emails(email_ids))

    @mcp.tool()
    @handle_errors
    async def move_email(email_id: str, target_folder: str) -> str:
        """Move an email to another folder. The target folder is created if it doesn't exist."""
        return dumps(email_service.move_email(email_id, target_folder))

    @mcp.tool()
    @handle_errors
    async def move_emails(email_ids: List[str], target_folder: str) -> str:
        """Move multiple emails to another folder in one call."""
        return dumps(email_service.move_emails(email_ids, target_folder))

    @mcp.tool()
    @handle_errors
    async def mark_emails(email_ids: List[str], status: str) -> str:
        """Mark emails with status `read`, `unread`, `important`, or `not_important`."""
        return dumps(email_service.mark_emails(email_ids, status))
