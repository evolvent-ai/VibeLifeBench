"""CRUD operations on advisories, advisory_subscriptions, notifications."""

import json
from typing import List, Optional

from ..models.advisory import Advisory, AdvisorySubscription, Notification
from .sqlite_backend import SqliteBackend


def _row_to_advisory(row) -> Advisory:
    return Advisory(
        country_code=row["country_code"],
        level=int(row["level"]),
        text=row["text"],
        updated_at=row["updated_at"],
    )


def _row_to_subscription(row) -> AdvisorySubscription:
    return AdvisorySubscription(
        sub_id=row["sub_id"],
        country_code=row["country_code"],
        sink=row["sink"],
        created_at=row["created_at"],
    )


def _row_to_notification(row) -> Notification:
    return Notification(
        id=row["id"],
        created_at=row["created_at"],
        channel=row["channel"],
        payload=json.loads(row["payload_json"] or "{}"),
    )


class AdvisoryBackend:
    def __init__(self, backend: SqliteBackend):
        self.backend = backend

    # ---- advisories --------------------------------------------------------

    def get(self, country_code: str) -> Optional[Advisory]:
        row = self.backend.fetchone(
            "SELECT * FROM advisories WHERE country_code = ?",
            (country_code,),
        )
        return _row_to_advisory(row) if row else None

    def upsert(self, advisory: Advisory) -> None:
        self.backend.execute(
            "INSERT INTO advisories(country_code, level, text, updated_at) "
            "VALUES(?, ?, ?, ?) "
            "ON CONFLICT(country_code) DO UPDATE SET "
            " level = excluded.level,"
            " text = excluded.text,"
            " updated_at = excluded.updated_at",
            (
                advisory.country_code,
                int(advisory.level),
                advisory.text,
                advisory.updated_at,
            ),
        )

    def insert_or_ignore(self, advisory: Advisory) -> None:
        self.backend.execute(
            "INSERT OR IGNORE INTO advisories(country_code, level, text, updated_at) "
            "VALUES(?, ?, ?, ?)",
            (
                advisory.country_code,
                int(advisory.level),
                advisory.text,
                advisory.updated_at,
            ),
        )

    def list_all(self) -> List[Advisory]:
        rows = self.backend.fetchall("SELECT * FROM advisories ORDER BY country_code ASC")
        return [_row_to_advisory(r) for r in rows]

    # ---- subscriptions -----------------------------------------------------

    def insert_subscription(self, sub: AdvisorySubscription) -> None:
        self.backend.execute(
            "INSERT INTO advisory_subscriptions(sub_id, country_code, sink, created_at) "
            "VALUES(?, ?, ?, ?)",
            (sub.sub_id, sub.country_code, sub.sink, sub.created_at),
        )

    def list_subscriptions_for(self, country_code: str) -> List[AdvisorySubscription]:
        rows = self.backend.fetchall(
            "SELECT * FROM advisory_subscriptions WHERE country_code = ? "
            "ORDER BY created_at ASC, sub_id ASC",
            (country_code,),
        )
        return [_row_to_subscription(r) for r in rows]

    # ---- notifications -----------------------------------------------------

    def insert_notification(self, notification: Notification) -> None:
        self.backend.execute(
            "INSERT INTO notifications(id, created_at, channel, payload_json) "
            "VALUES(?, ?, ?, ?)",
            (
                notification.id,
                notification.created_at,
                notification.channel,
                json.dumps(notification.payload),
            ),
        )

    def list_notifications(self, channel: Optional[str] = None) -> List[Notification]:
        if channel:
            rows = self.backend.fetchall(
                "SELECT * FROM notifications WHERE channel = ? ORDER BY id ASC",
                (channel,),
            )
        else:
            rows = self.backend.fetchall(
                "SELECT * FROM notifications ORDER BY id ASC"
            )
        return [_row_to_notification(r) for r in rows]
