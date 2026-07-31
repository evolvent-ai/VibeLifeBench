from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class EmailAttachment:
    """One attachment row from the ``attachments`` table.

    ``content`` is base64-encoded so JSON-emitting tools can pass it
    through unchanged. For binary downloads via ``download_attachment``
    the bytes are decoded on the fly.
    """
    attachment_id: str
    filename: str
    content_type: str
    size: int


@dataclass
class EmailFolder:
    name: str
    total_messages: int = 0
    unread_messages: int = 0
    can_select: bool = True


@dataclass
class EmailMessage:
    email_id: str
    subject: str
    from_addr: str
    to_addr: str
    cc_addr: Optional[str] = None
    bcc_addr: Optional[str] = None
    date: Optional[str] = None
    message_id: Optional[str] = None
    body_text: Optional[str] = None
    body_html: Optional[str] = None
    is_read: bool = False
    is_important: bool = False
    folder: Optional[str] = None
    attachments: List[EmailAttachment] = field(default_factory=list)
    headers: Optional[dict] = None
