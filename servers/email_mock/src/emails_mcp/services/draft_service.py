"""Draft CRUD persisted in the ``drafts`` table."""
import sqlite3
from typing import List, Optional

from ..utils.addrs import addrs_to_json, json_to_csv
from ..utils.dates import now_iso_z
from ..utils.exceptions import DraftNotFoundError
from ..utils.validators import validate_email_id, validate_page_params
from ._common import get_account_email


class DraftService:
    def __init__(self, conn: sqlite3.Connection) -> None:
        self.conn = conn

    # ---- create / update / delete --------------------------------------
    def save_draft(
        self,
        subject: str,
        body: str,
        html_body: Optional[str] = None,
        to: Optional[str] = None,
        cc: Optional[str] = None,
        bcc: Optional[str] = None,
        in_reply_to: Optional[str] = None,
    ) -> dict:
        now = now_iso_z()
        from_addr = get_account_email(self.conn)
        cur = self.conn.execute(
            """
            INSERT INTO drafts (
              subject, from_addr, to_addr_json, cc_addr_json, bcc_addr_json,
              body_text, body_html, in_reply_to, created_at, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                subject or "",
                from_addr,
                addrs_to_json(to),
                addrs_to_json(cc),
                addrs_to_json(bcc),
                body or "",
                html_body,
                in_reply_to,
                now,
                now,
            ),
        )
        return {"draft_id": str(int(cur.lastrowid)), "created_at": now, "updated_at": now}

    def update_draft(
        self,
        draft_id: str,
        subject: Optional[str] = None,
        body: Optional[str] = None,
        html_body: Optional[str] = None,
        to: Optional[str] = None,
        cc: Optional[str] = None,
        bcc: Optional[str] = None,
        in_reply_to: Optional[str] = None,
    ) -> dict:
        pk = validate_email_id(draft_id)
        sets: List[str] = ["updated_at = ?"]
        params: List = [now_iso_z()]
        if subject is not None:
            sets.append("subject = ?"); params.append(subject)
        if body is not None:
            sets.append("body_text = ?"); params.append(body)
        if html_body is not None:
            sets.append("body_html = ?"); params.append(html_body)
        if to is not None:
            sets.append("to_addr_json = ?"); params.append(addrs_to_json(to))
        if cc is not None:
            sets.append("cc_addr_json = ?"); params.append(addrs_to_json(cc))
        if bcc is not None:
            sets.append("bcc_addr_json = ?"); params.append(addrs_to_json(bcc))
        if in_reply_to is not None:
            sets.append("in_reply_to = ?"); params.append(in_reply_to)
        params.append(pk)
        cur = self.conn.execute(
            f"UPDATE drafts SET {', '.join(sets)} WHERE id = ?",
            params,
        )
        if cur.rowcount == 0:
            raise DraftNotFoundError(f"draft not found: {draft_id}")
        return {"draft_id": str(pk), "updated_at": params[0]}

    def delete_draft(self, draft_id: str) -> dict:
        pk = validate_email_id(draft_id)
        cur = self.conn.execute("DELETE FROM drafts WHERE id = ?", (pk,))
        if cur.rowcount == 0:
            raise DraftNotFoundError(f"draft not found: {draft_id}")
        return {"draft_id": str(pk), "deleted": True}

    # ---- read -----------------------------------------------------------
    def get_drafts(self, page: int = 1, page_size: int = 20) -> dict:
        p, ps = validate_page_params(page, page_size)
        total_row = self.conn.execute("SELECT COUNT(*) AS c FROM drafts").fetchone()
        total = int(total_row["c"] or 0)
        total_pages = max(1, (total + ps - 1) // ps) if total else 1
        if p > total_pages:
            p = total_pages
        offset = (p - 1) * ps
        rows = self.conn.execute(
            """
            SELECT id, subject, from_addr, to_addr_json, cc_addr_json, bcc_addr_json,
                   body_text, body_html, in_reply_to, created_at, updated_at
            FROM drafts ORDER BY updated_at DESC, id DESC LIMIT ? OFFSET ?
            """,
            (ps, offset),
        ).fetchall()
        return {
            "drafts": [self._row_to_dict(r) for r in rows],
            "total_drafts": total,
            "current_page": p,
            "total_pages": total_pages,
            "page_size": ps,
        }

    def get_draft(self, draft_id: str) -> dict:
        pk = validate_email_id(draft_id)
        row = self.conn.execute(
            """
            SELECT id, subject, from_addr, to_addr_json, cc_addr_json, bcc_addr_json,
                   body_text, body_html, in_reply_to, created_at, updated_at
            FROM drafts WHERE id = ?
            """,
            (pk,),
        ).fetchone()
        if not row:
            raise DraftNotFoundError(f"draft not found: {draft_id}")
        return self._row_to_dict(row)

    @staticmethod
    def _row_to_dict(r: sqlite3.Row) -> dict:
        return {
            "draft_id": str(int(r["id"])),
            "subject": r["subject"] or "",
            "from_addr": r["from_addr"] or "",
            "to_addr": json_to_csv(r["to_addr_json"]),
            "cc_addr": json_to_csv(r["cc_addr_json"]),
            "bcc_addr": json_to_csv(r["bcc_addr_json"]),
            "body_text": r["body_text"] or "",
            "body_html": r["body_html"],
            "in_reply_to": r["in_reply_to"],
            "created_at": r["created_at"],
            "updated_at": r["updated_at"],
        }
