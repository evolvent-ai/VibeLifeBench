"""Per-user saved-case library: save, list, annotate."""
import logging
import sqlite3
from typing import List

from ..backends.db import next_counter
from ..utils.dates import now_iso_z
from ..utils.exceptions import BadArgError, SavedCaseNotFoundError
from ..utils.ids import saved_id as make_saved_id
from ._common import case_summary_dict, fetch_case

logger = logging.getLogger(__name__)


class LibraryService:
    def __init__(self, conn: sqlite3.Connection) -> None:
        self.conn = conn

    # ---- save ------------------------------------------------------------
    def save_case(self, user_id: str, case_id: str) -> dict:
        if not user_id:
            raise BadArgError("user_id is required")
        fetch_case(self.conn, case_id)  # raises CASE_NOT_FOUND

        existing = self._fetch_saved(user_id, case_id)
        if existing is not None:
            return self._saved_dict(existing)

        seq = next_counter(self.conn, "saved_seq")
        new_id = make_saved_id(seq)
        saved_at = now_iso_z()
        self.conn.execute(
            """
            INSERT INTO saved_cases (saved_id, user_id, case_id, note, saved_at)
            VALUES (?, ?, ?, NULL, ?)
            """,
            (new_id, user_id, case_id, saved_at),
        )
        row = self._fetch_saved(user_id, case_id)
        return self._saved_dict(row)

    # ---- list ------------------------------------------------------------
    def list_saved(self, user_id: str) -> List[dict]:
        if not user_id:
            raise BadArgError("user_id is required")
        rows = self.conn.execute(
            """
            SELECT * FROM saved_cases WHERE user_id = ?
            ORDER BY saved_at ASC, saved_id ASC
            """,
            (user_id,),
        ).fetchall()
        out = []
        for r in rows:
            case_row = self.conn.execute(
                "SELECT * FROM cases WHERE case_id = ?", (r["case_id"],)
            ).fetchone()
            d = self._saved_dict(r)
            if case_row is not None:
                d["case"] = case_summary_dict(self.conn, case_row)
            out.append(d)
        return out

    # ---- note ------------------------------------------------------------
    def add_note_to_case(self, user_id: str, case_id: str, note: str) -> dict:
        if not user_id:
            raise BadArgError("user_id is required")
        if note is None:
            raise BadArgError("note is required")
        # auto-save on first note if not already saved
        if self._fetch_saved(user_id, case_id) is None:
            self.save_case(user_id, case_id)
        row = self._fetch_saved(user_id, case_id)
        if row is None:
            raise SavedCaseNotFoundError(
                f"no saved case for user {user_id} / case {case_id}"
            )
        self.conn.execute(
            "UPDATE saved_cases SET note = ? WHERE saved_id = ?",
            (note, row["saved_id"]),
        )
        return self._saved_dict(self._fetch_saved(user_id, case_id))

    # ---- helpers ---------------------------------------------------------
    def _fetch_saved(self, user_id: str, case_id: str):
        return self.conn.execute(
            "SELECT * FROM saved_cases WHERE user_id = ? AND case_id = ?",
            (user_id, case_id),
        ).fetchone()

    def _saved_dict(self, r: sqlite3.Row) -> dict:
        return {
            "saved_id": r["saved_id"],
            "user_id": r["user_id"],
            "case_id": r["case_id"],
            "note": r["note"],
            "saved_at": r["saved_at"],
        }
