"""Attachment download.

Attachments are stored as base64 strings in ``attachments.content_b64``.
``download_attachment`` decodes and writes them to a caller-supplied path.
"""
import base64
import os
import sqlite3
from pathlib import Path
from typing import Optional

from ..utils.exceptions import (
    AttachmentNotFoundError,
    BadArgError,
    FileError,
)
from ..utils.validators import validate_email_id
from ._common import fetch_message_row


class AttachmentService:
    def __init__(self, conn: sqlite3.Connection) -> None:
        self.conn = conn

    def download_attachment(
        self,
        email_id: str,
        attachment_filename: str,
        download_path: Optional[str] = None,
    ) -> dict:
        pk = validate_email_id(email_id)
        # Confirm the email exists; surfaces EMAIL_NOT_FOUND cleanly.
        fetch_message_row(self.conn, pk)

        if not attachment_filename or not isinstance(attachment_filename, str):
            raise BadArgError("attachment_filename is required")

        row = self.conn.execute(
            """
            SELECT id, filename, content_type, size, content_b64
            FROM attachments WHERE message_id = ? AND filename = ?
            ORDER BY id ASC LIMIT 1
            """,
            (pk, attachment_filename),
        ).fetchone()
        if not row:
            raise AttachmentNotFoundError(
                f"attachment '{attachment_filename}' not found in email {email_id}"
            )

        try:
            data = base64.b64decode(row["content_b64"] or "")
        except Exception as e:
            raise FileError(f"attachment payload not valid base64: {e}")

        dest_dir = Path(download_path) if download_path else Path.cwd()
        try:
            dest_dir.mkdir(parents=True, exist_ok=True)
        except OSError as e:
            raise FileError(f"cannot create download_path {dest_dir}: {e}")

        target = dest_dir / row["filename"]
        # Avoid overwrite — append (1)/(2)/… like the upstream behaviour.
        if target.exists():
            stem, ext = os.path.splitext(row["filename"])
            i = 1
            while True:
                candidate = dest_dir / f"{stem}({i}){ext}"
                if not candidate.exists():
                    target = candidate
                    break
                i += 1
        target.write_bytes(data)
        return {
            "email_id": str(pk),
            "filename": row["filename"],
            "content_type": row["content_type"] or "application/octet-stream",
            "size": int(row["size"] or len(data)),
            "saved_to": str(target),
        }
