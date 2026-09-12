"""CRUD operations on entry_requirements."""

import json
from typing import List, Optional

from ..models.entry import EntryRequirement
from .sqlite_backend import SqliteBackend


def _row_to_entry(row) -> EntryRequirement:
    return EntryRequirement(
        origin_nationality=row["origin_nationality"],
        destination=row["destination"],
        purpose=row["purpose"],
        visa_required=bool(row["visa_required"]),
        allowed_stay_days=int(row["allowed_stay_days"] or 0),
        passport_validity_months=int(row["passport_validity_months"]),
        docs_needed=json.loads(row["docs_needed_json"] or "[]"),
        notes=row["notes"] or "",
        updated_at=row["updated_at"],
    )


class EntryBackend:
    def __init__(self, backend: SqliteBackend):
        self.backend = backend

    def get(
        self, origin_nationality: str, destination: str, purpose: str
    ) -> Optional[EntryRequirement]:
        row = self.backend.fetchone(
            "SELECT * FROM entry_requirements "
            "WHERE origin_nationality = ? AND destination = ? AND purpose = ?",
            (origin_nationality, destination, purpose),
        )
        return _row_to_entry(row) if row else None

    def upsert(self, entry: EntryRequirement) -> None:
        self.backend.execute(
            "INSERT INTO entry_requirements("
            " origin_nationality, destination, purpose, visa_required,"
            " allowed_stay_days, passport_validity_months, docs_needed_json,"
            " notes, updated_at"
            ") VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?) "
            "ON CONFLICT(origin_nationality, destination, purpose) DO UPDATE SET "
            " visa_required = excluded.visa_required,"
            " allowed_stay_days = excluded.allowed_stay_days,"
            " passport_validity_months = excluded.passport_validity_months,"
            " docs_needed_json = excluded.docs_needed_json,"
            " notes = excluded.notes,"
            " updated_at = excluded.updated_at",
            (
                entry.origin_nationality,
                entry.destination,
                entry.purpose,
                1 if entry.visa_required else 0,
                int(entry.allowed_stay_days),
                int(entry.passport_validity_months),
                json.dumps(entry.docs_needed),
                entry.notes,
                entry.updated_at,
            ),
        )

    def insert_or_ignore(self, entry: EntryRequirement) -> None:
        self.backend.execute(
            "INSERT OR IGNORE INTO entry_requirements("
            " origin_nationality, destination, purpose, visa_required,"
            " allowed_stay_days, passport_validity_months, docs_needed_json,"
            " notes, updated_at"
            ") VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (
                entry.origin_nationality,
                entry.destination,
                entry.purpose,
                1 if entry.visa_required else 0,
                int(entry.allowed_stay_days),
                int(entry.passport_validity_months),
                json.dumps(entry.docs_needed),
                entry.notes,
                entry.updated_at,
            ),
        )

    def list_all(self) -> List[EntryRequirement]:
        rows = self.backend.fetchall("SELECT * FROM entry_requirements")
        return [_row_to_entry(r) for r in rows]
