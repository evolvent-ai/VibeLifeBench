"""Export / import.

- ``export_emails`` writes a single JSON file containing the selected
  messages (with attachments inlined as base64).
- ``import_emails`` reads such a JSON file back and inserts the messages
  into the requested folder.

Both operations are constrained to the local filesystem the server can
see — no remote URLs, no network access.
"""
import base64
import json
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import List, Optional

from ..backends.db import next_counter
from ..utils.addrs import addrs_to_json, json_to_csv
from ..utils.dates import now_iso_z
from ..utils.exceptions import BadArgError, FileError, FolderNotFoundError
from ..utils.ids import message_id_header
from ..utils.validators import validate_folder_name
from ._common import (
    get_folder_id,
    get_or_create_folder_id,
    list_attachments,
    refresh_folder_counts,
)


class IOService:
    def __init__(self, conn: sqlite3.Connection) -> None:
        self.conn = conn

    # ---- export ---------------------------------------------------------
    def export_emails(
        self,
        folder: Optional[str] = None,
        export_path: str = "emails_export.json",
        max_emails: Optional[int] = None,
        export_all_folders: bool = False,
    ) -> dict:
        if export_all_folders and folder:
            raise BadArgError(
                "cannot specify both `folder` and `export_all_folders=True`"
            )
        # Determine which folder ids to pull from.
        if export_all_folders:
            rows = self.conn.execute("SELECT id, name FROM folders ORDER BY name").fetchall()
            targets = [(int(r["id"]), r["name"]) for r in rows]
        else:
            name = validate_folder_name(folder) if folder else "INBOX"
            fid = get_folder_id(self.conn, name)
            targets = [(fid, name)]

        all_messages: List[dict] = []
        folder_stats: dict = {}
        limit = int(max_emails) if max_emails else None
        for fid, fname in targets:
            remaining = (limit - len(all_messages)) if limit is not None else None
            if remaining is not None and remaining <= 0:
                break
            sql = (
                "SELECT * FROM messages WHERE folder_id = ? "
                "ORDER BY date ASC, id ASC"
            )
            params: List = [fid]
            if remaining is not None:
                sql += " LIMIT ?"
                params.append(remaining)
            rows = self.conn.execute(sql, params).fetchall()
            for r in rows:
                all_messages.append(self._row_to_export_dict(r, fname))
            folder_stats[fname] = len(rows)

        if not all_messages:
            raise BadArgError("no emails to export from the selected folders")

        path = Path(export_path)
        try:
            if path.parent and not path.parent.exists():
                path.parent.mkdir(parents=True, exist_ok=True)
        except OSError as e:
            raise FileError(f"cannot prepare export directory: {e}")
        payload = {
            "export_date": datetime.utcnow().isoformat() + "Z",
            "total_emails": len(all_messages),
            "folder_stats": folder_stats,
            "emails": all_messages,
        }
        try:
            path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        except OSError as e:
            raise FileError(f"failed writing export file {path}: {e}")
        return {
            "exported_path": str(path),
            "total_emails": len(all_messages),
            "folder_stats": folder_stats,
        }

    def _row_to_export_dict(self, r: sqlite3.Row, folder_name: str) -> dict:
        message_pk = int(r["id"])
        atts_meta = self.conn.execute(
            "SELECT filename, content_type, size, content_b64 FROM attachments WHERE message_id = ? ORDER BY id ASC",
            (message_pk,),
        ).fetchall()
        return {
            "email_id": str(message_pk),
            "folder": folder_name,
            "subject": r["subject"] or "",
            "from_addr": r["from_addr"] or "",
            "to_addr": json_to_csv(r["to_addr_json"]),
            "cc_addr": json_to_csv(r["cc_addr_json"]),
            "bcc_addr": json_to_csv(r["bcc_addr_json"]),
            "date": r["date"],
            "message_id": r["message_id"],
            "body_text": r["body_text"],
            "body_html": r["body_html"],
            "is_read": bool(int(r["is_read"])),
            "is_important": bool(int(r["is_important"])),
            "attachments": [
                {
                    "filename": a["filename"],
                    "content_type": a["content_type"],
                    "size": int(a["size"] or 0),
                    "content_b64": a["content_b64"] or "",
                }
                for a in atts_meta
            ],
        }

    # ---- import ---------------------------------------------------------
    def import_emails(
        self,
        import_path: str,
        target_folder: Optional[str] = None,
        preserve_folders: bool = True,
    ) -> dict:
        path = Path(import_path)
        if not path.exists() or not path.is_file():
            raise FileError(f"import file not found: {import_path}")
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as e:
            raise FileError(f"could not parse {import_path}: {e}")
        emails = payload.get("emails")
        if not isinstance(emails, list):
            raise FileError("import file missing 'emails' list")

        imported: List[str] = []
        failed: List[dict] = []
        folder_stats: dict = {}
        fallback = validate_folder_name(target_folder) if target_folder else "INBOX"
        for e in emails:
            try:
                folder_name = (
                    e.get("folder") if preserve_folders and e.get("folder") else fallback
                )
                folder_name = validate_folder_name(folder_name)
                folder_id = get_or_create_folder_id(self.conn, folder_name)
                now = now_iso_z()
                seq = next_counter(self.conn, "msg_seq")
                msg_hdr = e.get("message_id") or message_id_header(seq)
                cur = self.conn.execute(
                    """
                    INSERT INTO messages (
                      folder_id, message_id, subject, from_addr,
                      to_addr_json, cc_addr_json, bcc_addr_json,
                      date, body_text, body_html, is_read, is_important,
                      headers_json, size, created_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, '{}', ?, ?)
                    """,
                    (
                        folder_id,
                        msg_hdr,
                        e.get("subject") or "",
                        e.get("from_addr") or "",
                        addrs_to_json(e.get("to_addr")),
                        addrs_to_json(e.get("cc_addr")),
                        addrs_to_json(e.get("bcc_addr")),
                        e.get("date") or now,
                        e.get("body_text"),
                        e.get("body_html"),
                        1 if e.get("is_read") else 0,
                        1 if e.get("is_important") else 0,
                        len((e.get("body_text") or "")) + len((e.get("body_html") or "")),
                        now,
                    ),
                )
                new_id = int(cur.lastrowid)
                for a in e.get("attachments") or []:
                    self.conn.execute(
                        """
                        INSERT INTO attachments (message_id, filename, content_type, size, content_b64)
                        VALUES (?, ?, ?, ?, ?)
                        """,
                        (
                            new_id,
                            a.get("filename") or "attachment",
                            a.get("content_type") or "application/octet-stream",
                            int(a.get("size") or 0),
                            a.get("content_b64") or "",
                        ),
                    )
                refresh_folder_counts(self.conn, folder_id)
                imported.append(str(new_id))
                folder_stats[folder_name] = folder_stats.get(folder_name, 0) + 1
            except Exception as exc:  # noqa: BLE001
                failed.append({"email": e.get("email_id"), "error": str(exc)})

        return {
            "imported": imported,
            "failed": failed,
            "total": len(emails),
            "folder_stats": folder_stats,
        }
