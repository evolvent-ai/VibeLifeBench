"""Folder CRUD + stats."""
import sqlite3
from typing import List, Optional

from ..utils.exceptions import (
    FolderExistsError,
    FolderNotFoundError,
    FolderProtectedError,
)
from ..utils.validators import validate_folder_name
from ._common import (
    get_folder_id,
    get_or_create_folder_id,
    refresh_folder_counts,
)

SYSTEM_FOLDERS = ("INBOX", "Sent", "Drafts", "Trash", "Spam")


class FolderService:
    def __init__(self, conn: sqlite3.Connection) -> None:
        self.conn = conn

    # ---- list / stats ---------------------------------------------------
    def list_folders(self) -> List[dict]:
        rows = self.conn.execute(
            "SELECT id, name FROM folders ORDER BY name ASC"
        ).fetchall()
        out: List[dict] = []
        for r in rows:
            folder_id = int(r["id"])
            refresh_folder_counts(self.conn, folder_id)
            counts = self.conn.execute(
                "SELECT message_count, unread_count FROM folders WHERE id = ?",
                (folder_id,),
            ).fetchone()
            out.append(
                {
                    "name": r["name"],
                    "total_messages": int(counts["message_count"] or 0),
                    "unread_messages": int(counts["unread_count"] or 0),
                    "can_select": True,
                }
            )
        return out

    def get_folder_stats(self, folder_name: Optional[str]) -> dict:
        if folder_name:
            name = validate_folder_name(folder_name)
            folder_id = get_folder_id(self.conn, name)
            refresh_folder_counts(self.conn, folder_id)
            row = self.conn.execute(
                "SELECT message_count, unread_count FROM folders WHERE id = ?",
                (folder_id,),
            ).fetchone()
            return {
                "folder_name": name,
                "total_messages": int(row["message_count"] or 0),
                "unread_messages": int(row["unread_count"] or 0),
            }
        # aggregate across all folders
        folders = self.list_folders()
        total = sum(f["total_messages"] for f in folders)
        unread = sum(f["unread_messages"] for f in folders)
        return {
            "folder_name": None,
            "folders": folders,
            "total_messages": total,
            "unread_messages": unread,
        }

    def get_unread_count(self, folder_name: Optional[str]) -> dict:
        if folder_name:
            name = validate_folder_name(folder_name)
            folder_id = get_folder_id(self.conn, name)
            refresh_folder_counts(self.conn, folder_id)
            row = self.conn.execute(
                "SELECT unread_count FROM folders WHERE id = ?", (folder_id,)
            ).fetchone()
            return {"folder_name": name, "unread_messages": int(row["unread_count"] or 0)}
        # aggregate
        folders = self.list_folders()
        return {
            "folder_name": None,
            "unread_messages": sum(f["unread_messages"] for f in folders),
        }

    # ---- mutations ------------------------------------------------------
    def create_folder(self, folder_name: str) -> dict:
        name = validate_folder_name(folder_name)
        row = self.conn.execute(
            "SELECT id FROM folders WHERE name = ?", (name,)
        ).fetchone()
        if row:
            raise FolderExistsError(f"folder already exists: {name}")
        cur = self.conn.execute("INSERT INTO folders (name) VALUES (?)", (name,))
        return {"folder_name": name, "folder_id": int(cur.lastrowid)}

    def delete_folder(self, folder_name: str) -> dict:
        name = validate_folder_name(folder_name)
        if name in SYSTEM_FOLDERS:
            raise FolderProtectedError(f"cannot delete system folder: {name}")
        folder_id = get_folder_id(self.conn, name)
        # ON DELETE CASCADE on messages → attachments will also cascade.
        self.conn.execute("DELETE FROM folders WHERE id = ?", (folder_id,))
        return {"folder_name": name, "deleted": True}

    # ---- internal: ensure system folders exist --------------------------
    def ensure_system_folders(self) -> None:
        """Idempotently create the system folders the agent expects."""
        for name in SYSTEM_FOLDERS:
            get_or_create_folder_id(self.conn, name)
