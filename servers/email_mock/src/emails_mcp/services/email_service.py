"""Core email tools — get / read / search / send / reply / forward / move /
delete / mark / headers.

All state lives in SQLite. There is no IMAP / SMTP — outgoing mail is
written into the ``Sent`` folder and logged in ``sent_log``.
"""
import json
import logging
import sqlite3
from typing import List, Optional

from ..backends.db import next_counter
from ..utils.addrs import addrs_to_json, parse_addr_list, json_to_csv
from ..utils.dates import now_iso_z
from ..utils.exceptions import (
    BadArgError,
    EmailNotFoundError,
    FolderNotFoundError,
)
from ..utils.ids import message_id_header
from ..utils.validators import (
    validate_email_id,
    validate_folder_name,
    validate_page_params,
    validate_query,
)
from ._common import (
    fetch_message_row,
    get_account_email,
    get_folder_id,
    get_or_create_folder_id,
    message_row_to_dict,
    parse_status_arg,
    refresh_folder_counts,
)

logger = logging.getLogger(__name__)


class EmailService:
    def __init__(self, conn: sqlite3.Connection) -> None:
        self.conn = conn

    # ---- check_connection ----------------------------------------------
    def check_connection(self) -> dict:
        # Trivial in mock mode — if we can run a query, we're connected.
        self.conn.execute("SELECT 1").fetchone()
        return {
            "imap_ok": True,
            "smtp_ok": True,
            "backend": "sqlite",
            "account": get_account_email(self.conn),
        }

    # ---- listing / reading ---------------------------------------------
    def get_emails(self, folder: str = "INBOX", page: int = 1, page_size: int = 20) -> dict:
        name = validate_folder_name(folder)
        folder_id = get_folder_id(self.conn, name)
        refresh_folder_counts(self.conn, folder_id)
        p, ps = validate_page_params(page, page_size)

        total_row = self.conn.execute(
            "SELECT COUNT(*) AS c FROM messages WHERE folder_id = ?", (folder_id,)
        ).fetchone()
        total = int(total_row["c"] or 0)
        total_pages = max(1, (total + ps - 1) // ps) if total else 1
        if p > total_pages:
            p = total_pages
        offset = (p - 1) * ps

        rows = self.conn.execute(
            """
            SELECT m.*, f.name AS folder_name
            FROM messages m JOIN folders f ON f.id = m.folder_id
            WHERE m.folder_id = ?
            ORDER BY m.date DESC, m.id DESC
            LIMIT ? OFFSET ?
            """,
            (folder_id, ps, offset),
        ).fetchall()
        emails = [
            message_row_to_dict(self.conn, r, include_body=False)
            for r in rows
        ]
        return {
            "folder": name,
            "emails": emails,
            "total_results": total,
            "current_page": p,
            "total_pages": total_pages,
            "page_size": ps,
        }

    def read_email(self, email_id: str) -> dict:
        pk = validate_email_id(email_id)
        row = fetch_message_row(self.conn, pk)
        result = message_row_to_dict(self.conn, row, include_body=True)
        # Mark as read on read (matches upstream behaviour).
        self.conn.execute("UPDATE messages SET is_read = 1 WHERE id = ?", (pk,))
        refresh_folder_counts(self.conn, int(row["folder_id"]))
        result["is_read"] = True
        return result

    def get_email_headers(self, email_id: str) -> dict:
        pk = validate_email_id(email_id)
        row = fetch_message_row(self.conn, pk)
        return message_row_to_dict(
            self.conn, row, include_body=False, include_attachments=False, include_headers=True
        )

    # ---- search ---------------------------------------------------------
    def search_emails(
        self,
        query: str,
        folder: Optional[str] = None,
        page: int = 1,
        page_size: int = 20,
    ) -> dict:
        q = validate_query(query)
        p, ps = validate_page_params(page, page_size)

        params: List = []
        sql = (
            "SELECT m.*, f.name AS folder_name FROM messages m "
            "JOIN folders f ON f.id = m.folder_id WHERE "
        )
        if folder:
            name = validate_folder_name(folder)
            folder_id = get_folder_id(self.conn, name)
            sql += "m.folder_id = ? AND "
            params.append(folder_id)

        like = f"%{q}%"
        sql += (
            "(m.subject LIKE ? OR m.body_text LIKE ? OR m.from_addr LIKE ?) "
            "ORDER BY m.date DESC, m.id DESC"
        )
        params.extend([like, like, like])

        rows = self.conn.execute(sql, params).fetchall()
        total = len(rows)
        total_pages = max(1, (total + ps - 1) // ps) if total else 1
        if p > total_pages:
            p = total_pages
        offset = (p - 1) * ps
        page_rows = rows[offset : offset + ps]
        return {
            "query": q,
            "folder": folder,
            "emails": [
                message_row_to_dict(self.conn, r, include_body=False) for r in page_rows
            ],
            "total_results": total,
            "current_page": p,
            "total_pages": total_pages,
            "page_size": ps,
        }

    # ---- sending --------------------------------------------------------
    def send_email(
        self,
        to: str,
        subject: str,
        body: str,
        html_body: Optional[str] = None,
        cc: Optional[str] = None,
        bcc: Optional[str] = None,
    ) -> dict:
        if not to:
            raise BadArgError("`to` is required")
        from_addr = get_account_email(self.conn)
        sent_folder_id = get_or_create_folder_id(self.conn, "Sent")
        now = now_iso_z()
        seq = next_counter(self.conn, "msg_seq")
        msg_id = message_id_header(seq)

        size = len(body or "") + len(html_body or "")
        cur = self.conn.execute(
            """
            INSERT INTO messages (
              folder_id, message_id, subject, from_addr,
              to_addr_json, cc_addr_json, bcc_addr_json,
              date, body_text, body_html, is_read, is_important,
              headers_json, size, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 1, 0, '{}', ?, ?)
            """,
            (
                sent_folder_id,
                msg_id,
                subject or "",
                from_addr,
                addrs_to_json(to),
                addrs_to_json(cc),
                addrs_to_json(bcc),
                now,
                body or "",
                html_body,
                size,
                now,
            ),
        )
        new_id = int(cur.lastrowid)
        self.conn.execute(
            "INSERT INTO sent_log (message_id, sent_at) VALUES (?, ?)",
            (new_id, now),
        )
        refresh_folder_counts(self.conn, sent_folder_id)
        return {
            "email_id": str(new_id),
            "message_id": msg_id,
            "folder": "Sent",
            "to": to,
            "subject": subject or "",
            "date": now,
        }

    def reply_email(
        self,
        email_id: str,
        body: str,
        html_body: Optional[str] = None,
        cc: Optional[str] = None,
        bcc: Optional[str] = None,
        reply_all: bool = False,
    ) -> dict:
        pk = validate_email_id(email_id)
        row = fetch_message_row(self.conn, pk)
        original_subject = row["subject"] or ""
        reply_subject = (
            original_subject
            if original_subject.startswith("Re:")
            else f"Re: {original_subject}"
        )
        reply_to = row["from_addr"] or ""
        if not reply_to:
            raise BadArgError("original email has no sender to reply to")

        # reply_all: union of original To and CC, minus our own address.
        reply_cc = cc
        if reply_all:
            our_email = get_account_email(self.conn).lower()
            recips: List[str] = []
            recips.extend(parse_addr_list(json_to_csv(row["to_addr_json"])))
            recips.extend(parse_addr_list(json_to_csv(row["cc_addr_json"])))
            recips = [a for a in recips if our_email not in a.lower()]
            if cc:
                recips.extend(parse_addr_list(cc))
            # dedupe preserving order
            seen = set()
            ordered: List[str] = []
            for a in recips:
                if a.lower() not in seen:
                    seen.add(a.lower())
                    ordered.append(a)
            reply_cc = ", ".join(ordered) if ordered else None

        quoted = row["body_text"] or ""
        full_body = (
            f"{body}\n\n--- Original Message ---\n"
            f"From: {row['from_addr']}\nDate: {row['date']}\nSubject: {original_subject}\n\n"
            f"{quoted}"
        )
        full_html = None
        if html_body:
            quoted_html = row["body_html"] or quoted
            full_html = (
                f"{html_body}<br><br><hr><b>Original Message:</b><br>"
                f"From: {row['from_addr']}<br>Date: {row['date']}<br>"
                f"Subject: {original_subject}<br><br>{quoted_html}"
            )
        result = self.send_email(
            to=reply_to,
            subject=reply_subject,
            body=full_body,
            html_body=full_html,
            cc=reply_cc,
            bcc=bcc,
        )
        # Stamp in_reply_to on the new sent message so threading works.
        self.conn.execute(
            "UPDATE messages SET in_reply_to = ? WHERE id = ?",
            (row["message_id"], int(result["email_id"])),
        )
        result["in_reply_to"] = row["message_id"]
        return result

    def forward_email(
        self,
        email_id: str,
        to: str,
        body: Optional[str] = None,
        html_body: Optional[str] = None,
        cc: Optional[str] = None,
        bcc: Optional[str] = None,
    ) -> dict:
        pk = validate_email_id(email_id)
        row = fetch_message_row(self.conn, pk)
        original_subject = row["subject"] or ""
        fwd_subject = (
            original_subject
            if original_subject.startswith("Fwd:")
            else f"Fwd: {original_subject}"
        )
        quoted = row["body_text"] or ""
        full_body = (
            f"{body or ''}\n\n--- Forwarded Message ---\n"
            f"From: {row['from_addr']}\nTo: {json_to_csv(row['to_addr_json'])}\n"
            f"Date: {row['date']}\nSubject: {original_subject}\n\n{quoted}"
        )
        full_html = None
        if html_body or row["body_html"]:
            quoted_html = row["body_html"] or quoted
            full_html = (
                f"{html_body or ''}<br><br><hr><b>Forwarded Message:</b><br>"
                f"From: {row['from_addr']}<br>To: {json_to_csv(row['to_addr_json'])}<br>"
                f"Date: {row['date']}<br>Subject: {original_subject}<br><br>{quoted_html}"
            )
        result = self.send_email(
            to=to,
            subject=fwd_subject,
            body=full_body,
            html_body=full_html,
            cc=cc,
            bcc=bcc,
        )
        # Carry the original's attachments over to the forward.
        atts = self.conn.execute(
            "SELECT filename, content_type, size, content_b64, content_id FROM attachments WHERE message_id = ?",
            (pk,),
        ).fetchall()
        for a in atts:
            self.conn.execute(
                """
                INSERT INTO attachments (message_id, filename, content_type, size, content_b64, content_id)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    int(result["email_id"]),
                    a["filename"],
                    a["content_type"],
                    int(a["size"] or 0),
                    a["content_b64"],
                    a["content_id"],
                ),
            )
        result["forwarded_attachments"] = len(atts)
        return result

    # ---- mutate flags / location ---------------------------------------
    def delete_email(self, email_id: str) -> dict:
        pk = validate_email_id(email_id)
        row = fetch_message_row(self.conn, pk)
        folder_id = int(row["folder_id"])
        self.conn.execute("DELETE FROM messages WHERE id = ?", (pk,))
        refresh_folder_counts(self.conn, folder_id)
        return {"email_id": str(pk), "deleted": True}

    def delete_emails(self, email_ids: List[str]) -> dict:
        if not isinstance(email_ids, list):
            raise BadArgError("email_ids must be a list of strings")
        success: List[str] = []
        failed: List[dict] = []
        for eid in email_ids:
            try:
                self.delete_email(eid)
                success.append(str(eid))
            except Exception as e:
                failed.append({"email_id": str(eid), "error": str(e)})
        return {"deleted": success, "failed": failed, "total": len(email_ids)}

    def move_email(self, email_id: str, target_folder: str) -> dict:
        pk = validate_email_id(email_id)
        target_name = validate_folder_name(target_folder)
        target_id = get_or_create_folder_id(self.conn, target_name)
        row = fetch_message_row(self.conn, pk)
        old_folder_id = int(row["folder_id"])
        self.conn.execute(
            "UPDATE messages SET folder_id = ? WHERE id = ?", (target_id, pk)
        )
        refresh_folder_counts(self.conn, old_folder_id)
        refresh_folder_counts(self.conn, target_id)
        return {"email_id": str(pk), "target_folder": target_name}

    def move_emails(self, email_ids: List[str], target_folder: str) -> dict:
        if not isinstance(email_ids, list):
            raise BadArgError("email_ids must be a list of strings")
        target_name = validate_folder_name(target_folder)
        # validate folder exists once
        get_or_create_folder_id(self.conn, target_name)
        success: List[str] = []
        failed: List[dict] = []
        for eid in email_ids:
            try:
                self.move_email(eid, target_name)
                success.append(str(eid))
            except Exception as e:
                failed.append({"email_id": str(eid), "error": str(e)})
        return {
            "moved": success,
            "failed": failed,
            "target_folder": target_name,
            "total": len(email_ids),
        }

    def mark_emails(self, email_ids: List[str], status: str) -> dict:
        if not isinstance(email_ids, list):
            raise BadArgError("email_ids must be a list of strings")
        s = parse_status_arg(status)
        if s == "read":
            col, val = "is_read", 1
        elif s == "unread":
            col, val = "is_read", 0
        elif s == "important":
            col, val = "is_important", 1
        else:  # not_important
            col, val = "is_important", 0
        success: List[str] = []
        failed: List[dict] = []
        for eid in email_ids:
            try:
                pk = validate_email_id(eid)
                row = self.conn.execute(
                    "SELECT folder_id FROM messages WHERE id = ?", (pk,)
                ).fetchone()
                if not row:
                    raise EmailNotFoundError(f"email not found: {eid}")
                self.conn.execute(
                    f"UPDATE messages SET {col} = ? WHERE id = ?", (val, pk)
                )
                refresh_folder_counts(self.conn, int(row["folder_id"]))
                success.append(str(pk))
            except Exception as e:
                failed.append({"email_id": str(eid), "error": str(e)})
        return {
            "marked": success,
            "failed": failed,
            "status": s,
            "total": len(email_ids),
        }
