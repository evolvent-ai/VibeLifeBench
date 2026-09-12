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

        # The stored filename is caller-controlled (import_emails accepts it
        # unvalidated), so it must not be able to steer the write out of
        # dest_dir: a name containing parent-directory segments would otherwise
        # resolve outside it and be written there. Keep the last component only.
        safe_name = os.path.basename(str(row["filename"]).replace("\\", "/")).strip()
        if not safe_name or safe_name in (".", ".."):
            raise FileError(f"attachment has an unusable filename: {row['filename']!r}")

        target = dest_dir / safe_name
        # Avoid overwrite — append (1)/(2)/… like the upstream behaviour.
        if target.exists():
            stem, ext = os.path.splitext(safe_name)
            i = 1
            while True:
                candidate = dest_dir / f"{stem}({i}){ext}"
                if not candidate.exists():
                    target = candidate
                    break
                i += 1
        # Defence in depth: confirm the resolved path is still inside dest_dir
        # before writing (catches symlinked dest_dir components too).
        try:
            resolved_dir = dest_dir.resolve()
            if resolved_dir not in target.resolve().parents:
                raise FileError(f"refusing to write outside {resolved_dir}")
        except OSError as e:
            raise FileError(f"cannot resolve download target: {e}")
        target.write_bytes(data)
        return {
            "email_id": str(pk),
            "filename": row["filename"],
            "content_type": row["content_type"] or "application/octet-stream",
            # Bytes actually written, not the declared size: base64 decoding is
            # lenient, so a corrupt payload writes fewer bytes than the stored
            # size claims and the caller would never learn the file is short.
            "size": len(data),
            "saved_to": str(target),
        }
