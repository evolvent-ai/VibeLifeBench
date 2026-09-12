"""Shared SQL helpers used by the services."""
import json
import sqlite3
from typing import List, Optional

from ..utils.exceptions import EmailNotFoundError, FolderNotFoundError


def get_account_email(conn: sqlite3.Connection) -> str:
    """Return the configured account email (used as ``From:`` on outbound mail).

    If the env doesn't seed ``account_config``, fall back to a placeholder.
    """
    row = conn.execute(
        "SELECT email FROM account_config ORDER BY id ASC LIMIT 1"
    ).fetchone()
    if not row:
        return "user@mock.local"
    return row["email"]


def get_folder_id(conn: sqlite3.Connection, name: str) -> int:
    row = conn.execute(
        "SELECT id FROM folders WHERE name = ?", (name,)
    ).fetchone()
    if not row:
        raise FolderNotFoundError(f"folder not found: {name}")
    return int(row["id"])


def get_or_create_folder_id(conn: sqlite3.Connection, name: str) -> int:
    row = conn.execute(
        "SELECT id FROM folders WHERE name = ?", (name,)
    ).fetchone()
    if row:
        return int(row["id"])
    cur = conn.execute(
        "INSERT INTO folders (name) VALUES (?)",
        (name,),
    )
    return int(cur.lastrowid)


def refresh_folder_counts(conn: sqlite3.Connection, folder_id: int) -> None:
    conn.execute(
        """
        UPDATE folders SET
          message_count = (SELECT COUNT(*) FROM messages WHERE folder_id = ?),
          unread_count  = (SELECT COUNT(*) FROM messages WHERE folder_id = ? AND is_read = 0)
        WHERE id = ?
        """,
        (folder_id, folder_id, folder_id),
    )


def fetch_message_row(conn: sqlite3.Connection, message_pk: int) -> sqlite3.Row:
    row = conn.execute(
        """
        SELECT m.*, f.name AS folder_name
        FROM messages m
        JOIN folders f ON f.id = m.folder_id
        WHERE m.id = ?
        """,
        (message_pk,),
    ).fetchone()
    if not row:
        raise EmailNotFoundError(f"email not found: {message_pk}")
    return row


def list_attachments(conn: sqlite3.Connection, message_pk: int) -> List[dict]:
    rows = conn.execute(
        "SELECT id, filename, content_type, size FROM attachments WHERE message_id = ? ORDER BY id ASC",
        (message_pk,),
    ).fetchall()
    return [
        {
            "attachment_id": f"att_{int(r['id']):08d}",
            "filename": r["filename"],
            "content_type": r["content_type"] or "application/octet-stream",
            "size": int(r["size"] or 0),
        }
        for r in rows
    ]


def message_row_to_dict(
    conn: sqlite3.Connection,
    row: sqlite3.Row,
    *,
    include_body: bool = True,
    include_attachments: bool = True,
    include_headers: bool = False,
) -> dict:
    from ..utils.addrs import json_to_csv

    out = {
        "email_id": str(row["id"]),
        "folder": row["folder_name"],
        "subject": row["subject"] or "",
        "from_addr": row["from_addr"] or "",
        "to_addr": json_to_csv(row["to_addr_json"]),
        "cc_addr": json_to_csv(row["cc_addr_json"]),
        "bcc_addr": json_to_csv(row["bcc_addr_json"]),
        "date": row["date"],
        "message_id": row["message_id"],
        "is_read": bool(int(row["is_read"])),
        "is_important": bool(int(row["is_important"])),
    }
    if include_body:
        out["body_text"] = row["body_text"]
        out["body_html"] = row["body_html"]
    if include_attachments:
        out["attachments"] = list_attachments(conn, int(row["id"]))
    if include_headers:
        try:
            out["headers"] = json.loads(row["headers_json"] or "{}")
        except (json.JSONDecodeError, TypeError):
            out["headers"] = {}
        out["in_reply_to"] = row["in_reply_to"]
        out["references"] = row["references_header"]
    return out


def parse_status_arg(status: str) -> str:
    valid = {"read", "unread", "important", "not_important"}
    if status not in valid:
        from ..utils.exceptions import BadArgError
        raise BadArgError(
            "status must be one of: read, unread, important, not_important"
        )
    return status
